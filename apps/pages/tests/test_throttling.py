from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone as datetime_timezone
from threading import Barrier, Event, local
from unittest.mock import patch

from django.db import connections
from django.db.models.query import QuerySet
from django.test import (
    RequestFactory,
    SimpleTestCase,
    TestCase,
    TransactionTestCase,
    override_settings,
)

from apps.pages.models import ProjectInquiryThrottle
from apps.pages.throttling import (
    ProjectInquiryThrottleError,
    cleanup_expired_buckets,
    consume_project_inquiry_throttle,
    derive_bucket_key,
    resolve_client_address,
)


class ClientAddressResolutionTests(SimpleTestCase):
    def setUp(self):
        self.factory = RequestFactory()

    @override_settings(
        DEBUG=False,
        PROJECT_INQUIRY_TRUSTED_IP_HEADER="  Fly-Client-IP  ",
    )
    def test_uses_configured_header_and_normalizes_address(self):
        request = self.factory.get(
            "/",
            REMOTE_ADDR="192.0.2.10",
            HTTP_FLY_CLIENT_IP=(
                " 2001:0db8:0000:0000:0000:0000:0000:0001 "
            ),
        )

        self.assertEqual(resolve_client_address(request), "2001:db8::1")

    @override_settings(
        DEBUG=True,
        PROJECT_INQUIRY_TRUSTED_IP_HEADER="",
    )
    def test_uses_remote_address_only_in_debug(self):
        request = self.factory.get("/", REMOTE_ADDR=" 203.0.113.8 ")

        self.assertEqual(resolve_client_address(request), "203.0.113.8")

    def test_forwarded_for_cannot_override_authoritative_address(self):
        for debug, trusted_header, expected_address in (
            (False, "Fly-Client-IP", "203.0.113.20"),
            (True, "", "192.0.2.10"),
        ):
            for forwarded_for in (
                "198.51.100.8",
                "198.51.100.9, 198.51.100.10",
            ):
                with self.subTest(debug=debug, forwarded_for=forwarded_for):
                    with override_settings(
                        DEBUG=debug,
                        PROJECT_INQUIRY_TRUSTED_IP_HEADER=trusted_header,
                    ):
                        request = self.factory.get(
                            "/",
                            REMOTE_ADDR="192.0.2.10",
                            HTTP_FLY_CLIENT_IP="203.0.113.20",
                            HTTP_X_FORWARDED_FOR=forwarded_for,
                        )

                        self.assertEqual(
                            resolve_client_address(request), expected_address,
                        )

    @override_settings(
        DEBUG=False,
        PROJECT_INQUIRY_TRUSTED_IP_HEADER="",
    )
    def test_rejects_missing_production_header_configuration(self):
        request = self.factory.get("/", REMOTE_ADDR="203.0.113.8")

        with self.assertRaisesRegex(
            ProjectInquiryThrottleError,
            "trusted client IP header",
        ):
            resolve_client_address(request)

    @override_settings(
        DEBUG=False,
        PROJECT_INQUIRY_TRUSTED_IP_HEADER="Fly-Client-IP",
    )
    def test_rejects_missing_or_invalid_trusted_header_value(self):
        requests = (
            self.factory.get("/", REMOTE_ADDR="203.0.113.8"),
            self.factory.get(
                "/",
                REMOTE_ADDR="203.0.113.8",
                HTTP_FLY_CLIENT_IP="not-an-address",
            ),
            self.factory.get(
                "/",
                REMOTE_ADDR="203.0.113.8",
                HTTP_FLY_CLIENT_IP="203.0.113.20, 203.0.113.21",
                HTTP_X_FORWARDED_FOR="198.51.100.8",
            ),
        )

        for request in requests:
            with self.subTest(headers=dict(request.headers)):
                with self.assertRaisesRegex(
                    ProjectInquiryThrottleError,
                    "valid client network address",
                ):
                    resolve_client_address(request)


@override_settings(SECRET_KEY="test-throttle-secret")
class BucketKeyTests(SimpleTestCase):
    def test_key_is_stable_opaque_and_scoped_to_address_and_window(self):
        key = derive_bucket_key("2001:db8::1", 42)
        equivalent_key = derive_bucket_key(
            "2001:0db8:0000:0000:0000:0000:0000:0001",
            42,
        )

        self.assertEqual(key, equivalent_key)
        self.assertEqual(len(key), 64)
        self.assertNotIn("2001:db8::1", key)
        self.assertNotEqual(key, derive_bucket_key("2001:db8::2", 42))
        self.assertNotEqual(key, derive_bucket_key("2001:db8::1", 43))


@override_settings(
    DEBUG=True,
    PROJECT_INQUIRY_TRUSTED_IP_HEADER="",
    PROJECT_INQUIRY_THROTTLE_LIMIT=3,
    PROJECT_INQUIRY_THROTTLE_WINDOW_SECONDS=60,
)
class ThrottleConsumptionTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get("/", REMOTE_ADDR="203.0.113.20")
        self.now = datetime(
            2026,
            1,
            1,
            12,
            0,
            30,
            tzinfo=datetime_timezone.utc,
        )

    def test_claims_available_attempts_without_exceeding_limit(self):
        self.assertTrue(
            consume_project_inquiry_throttle(self.request, now=self.now)
        )
        self.assertTrue(
            consume_project_inquiry_throttle(self.request, now=self.now)
        )
        self.assertTrue(
            consume_project_inquiry_throttle(self.request, now=self.now)
        )
        self.assertFalse(
            consume_project_inquiry_throttle(self.request, now=self.now)
        )

        bucket = ProjectInquiryThrottle.objects.get()
        self.assertEqual(bucket.attempt_count, 3)
        self.assertEqual(
            bucket.expires_at,
            datetime(
                2026,
                1,
                1,
                12,
                1,
                tzinfo=datetime_timezone.utc,
            ),
        )

    def test_next_window_creates_a_new_bucket_and_expires_old_bucket(self):
        first_time = self.now + timedelta(seconds=29)
        self.assertTrue(
            consume_project_inquiry_throttle(
                self.request,
                now=first_time,
            )
        )
        first_key = ProjectInquiryThrottle.objects.get().bucket_key

        next_window = first_time + timedelta(seconds=1)
        self.assertTrue(
            consume_project_inquiry_throttle(
                self.request,
                now=next_window,
            )
        )

        current_bucket = ProjectInquiryThrottle.objects.get()
        self.assertNotEqual(current_bucket.bucket_key, first_key)
        self.assertEqual(current_bucket.attempt_count, 1)
        self.assertEqual(
            current_bucket.expires_at,
            datetime(
                2026,
                1,
                1,
                12,
                2,
                tzinfo=datetime_timezone.utc,
            ),
        )

    def test_rejects_invalid_limit_and_window_settings_before_writing(self):
        invalid_settings = (
            ("PROJECT_INQUIRY_THROTTLE_LIMIT", 0),
            ("PROJECT_INQUIRY_THROTTLE_LIMIT", -1),
            ("PROJECT_INQUIRY_THROTTLE_LIMIT", "1"),
            ("PROJECT_INQUIRY_THROTTLE_LIMIT", True),
            ("PROJECT_INQUIRY_THROTTLE_WINDOW_SECONDS", 0),
            ("PROJECT_INQUIRY_THROTTLE_WINDOW_SECONDS", -1),
            ("PROJECT_INQUIRY_THROTTLE_WINDOW_SECONDS", "60"),
            ("PROJECT_INQUIRY_THROTTLE_WINDOW_SECONDS", True),
        )

        for setting_name, value in invalid_settings:
            with self.subTest(setting=setting_name, value=value):
                with override_settings(**{setting_name: value}):
                    with self.assertRaises(ProjectInquiryThrottleError):
                        consume_project_inquiry_throttle(
                            self.request,
                            now=self.now,
                        )

        self.assertFalse(ProjectInquiryThrottle.objects.exists())

    def test_rejects_naive_clock_before_writing(self):
        with self.assertRaisesRegex(
            ProjectInquiryThrottleError,
            "aware datetime",
        ):
            consume_project_inquiry_throttle(
                self.request,
                now=datetime(2026, 1, 1, 12, 0, 30),
            )

        self.assertFalse(ProjectInquiryThrottle.objects.exists())


@override_settings(
    DEBUG=True,
    PROJECT_INQUIRY_TRUSTED_IP_HEADER="",
    PROJECT_INQUIRY_THROTTLE_LIMIT=1,
    PROJECT_INQUIRY_THROTTLE_WINDOW_SECONDS=60,
)
class ConcurrentThrottleConsumptionTests(TransactionTestCase):
    def setUp(self):
        self.now = datetime(
            2026, 1, 1, 12, 0, 30, tzinfo=datetime_timezone.utc,
        )

    def competing_claims(self):
        lookups_ready = Barrier(2, timeout=5)
        first_finished = Event()
        worker_state = local()
        original_get = QuerySet.get

        def synchronized_get(queryset, *args, **kwargs):
            synchronize = (
                queryset.model is ProjectInquiryThrottle
                and "bucket_key" in kwargs
                and not getattr(worker_state, "looked_up", True)
            )
            if not synchronize:
                return original_get(queryset, *args, **kwargs)

            worker_state.looked_up = True
            worker_state.observed_count = None
            try:
                bucket = original_get(queryset, *args, **kwargs)
                worker_state.observed_count = bucket.attempt_count
                return bucket
            finally:
                # Both workers read the old state. Order subsequent writes so
                # SQLite lock contention cannot obscure the stale-read race.
                lookups_ready.wait()
                if not worker_state.first:
                    self.assertTrue(first_finished.wait(timeout=5))

        def claim(first):
            worker_state.first = first
            worker_state.looked_up = False
            database = connections["default"]
            try:
                database.ensure_connection()
                connection_id = id(database.connection)
                request = RequestFactory().post(
                    "/", REMOTE_ADDR="203.0.113.20",
                )
                allowed = consume_project_inquiry_throttle(
                    request, now=self.now,
                )
                return allowed, connection_id, worker_state.observed_count
            finally:
                database.close()
                if first:
                    first_finished.set()

        with patch.object(QuerySet, "get", synchronized_get):
            with ThreadPoolExecutor(max_workers=2) as executor:
                futures = [
                    executor.submit(claim, first) for first in (True, False)
                ]
                results = [future.result(timeout=15) for future in futures]

        self.assertNotEqual(results[0][1], results[1][1])
        return results

    def test_concurrent_first_claims_create_only_one_allowed_attempt(self):
        results = self.competing_claims()

        self.assertEqual([result[2] for result in results], [None, None])
        self.assertEqual([result[0] for result in results], [True, False])
        self.assertEqual(ProjectInquiryThrottle.objects.get().attempt_count, 1)

    @override_settings(PROJECT_INQUIRY_THROTTLE_LIMIT=3)
    def test_concurrent_claims_cannot_both_take_last_available_attempt(self):
        bucket = ProjectInquiryThrottle.objects.create(
            bucket_key=derive_bucket_key(
                "203.0.113.20", int(self.now.timestamp()) // 60,
            ),
            attempt_count=2,
            expires_at=self.now + timedelta(seconds=30),
        )

        results = self.competing_claims()

        self.assertEqual([result[2] for result in results], [2, 2])
        self.assertEqual([result[0] for result in results], [True, False])
        self.assertEqual(ProjectInquiryThrottle.objects.count(), 1)
        bucket.refresh_from_db()
        self.assertEqual(bucket.attempt_count, 3)


class ExpiredBucketCleanupTests(TestCase):
    def test_cleanup_deletes_only_oldest_one_hundred_expired_buckets(self):
        current_time = datetime(
            2026,
            1,
            1,
            12,
            0,
            tzinfo=datetime_timezone.utc,
        )
        expired_buckets = [
            ProjectInquiryThrottle(
                bucket_key=f"{index:064x}",
                expires_at=current_time - timedelta(seconds=101 - index),
            )
            for index in range(101)
        ]
        ProjectInquiryThrottle.objects.bulk_create(expired_buckets)
        live_bucket = ProjectInquiryThrottle.objects.create(
            bucket_key="f" * 64,
            expires_at=current_time + timedelta(seconds=1),
        )

        removed_count = cleanup_expired_buckets(current_time)

        self.assertEqual(removed_count, 100)
        self.assertEqual(
            ProjectInquiryThrottle.objects.filter(
                expires_at__lte=current_time,
            ).count(),
            1,
        )
        self.assertTrue(
            ProjectInquiryThrottle.objects.filter(pk=live_bucket.pk).exists()
        )
        self.assertTrue(
            ProjectInquiryThrottle.objects.filter(
                bucket_key=f"{100:064x}",
            ).exists()
        )
