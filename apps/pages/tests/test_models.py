from datetime import timedelta

from django.db import IntegrityError, transaction
from django.test import TestCase
from django.utils import timezone

from apps.pages.models import ProjectInquiryThrottle


class ProjectInquiryThrottleModelTests(TestCase):
    def test_model_schema_matches_throttle_contract(self):
        model_meta = ProjectInquiryThrottle._meta
        bucket_key_field = model_meta.get_field("bucket_key")
        attempt_count_field = model_meta.get_field("attempt_count")
        expires_at_field = model_meta.get_field("expires_at")

        self.assertEqual(
            model_meta.db_table,
            "apps_pages_projectinquirythrottle",
        )
        self.assertEqual(bucket_key_field.max_length, 64)
        self.assertTrue(bucket_key_field.unique)
        self.assertEqual(attempt_count_field.default, 1)
        self.assertTrue(expires_at_field.db_index)

    def test_persists_bucket_with_default_count_and_expiry(self):
        bucket_key = "a" * 64
        expires_at = timezone.now() + timedelta(minutes=1)

        bucket = ProjectInquiryThrottle.objects.create(
            bucket_key=bucket_key,
            expires_at=expires_at,
        )
        bucket.refresh_from_db()

        self.assertEqual(bucket.bucket_key, bucket_key)
        self.assertEqual(bucket.attempt_count, 1)
        self.assertEqual(bucket.expires_at, expires_at)

    def test_bucket_key_is_unique(self):
        bucket_data = {
            "bucket_key": "b" * 64,
            "expires_at": timezone.now() + timedelta(minutes=1),
        }
        ProjectInquiryThrottle.objects.create(**bucket_data)

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                ProjectInquiryThrottle.objects.create(**bucket_data)
