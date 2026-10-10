from copy import deepcopy
import json
import logging
from unittest.mock import Mock, patch

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.transport import Transport

from django.conf import settings
from django.core.handlers.wsgi import WSGIHandler
from django.db import DatabaseError
from django.middleware.csrf import get_token
from django.test import (
    Client, RequestFactory, SimpleTestCase, TestCase, override_settings,
)
from django.urls import reverse

from apps.pages.throttling import ProjectInquiryThrottleError
from hrcodes.sentry_privacy import before_send


class InquirySentryPrivacyTests(SimpleTestCase):
    event_id = '0123456789abcdef0123456789abcdef'
    timestamp = '2026-10-09T12:34:56.123456Z'
    inquiry_logs = (
        ('Project inquiry throttle evaluation failed.', 'throttle'),
        ('Project inquiry email delivery failed.', 'email_delivery'),
    )

    def event(self, **overrides):
        event = {
            'event_id': self.event_id,
            'timestamp': self.timestamp,
            'level': 'error',
            'request': {'method': 'POST', 'url': 'https://example.test/'},
        }
        event.update(overrides)
        return event

    def diagnostic(self, category='other', level='error'):
        return {
            'event_id': self.event_id,
            'timestamp': self.timestamp,
            'level': level,
            'message': 'Project inquiry failed.',
            'tags': {'project_inquiry_failure': category},
            'fingerprint': ['project-inquiry', category],
        }

    def log_record(self, message, logger='apps.pages.views'):
        return logging.LogRecord(
            logger, logging.ERROR, __file__, 1, message, (), None,
        )

    def test_post_root_events_are_sanitized_including_query_urls(self):
        for url in (
            '/',
            '/?goal=PRIVATE_QUERY_MARKER',
            'https://example.test/',
            'https://example.test/?goal=PRIVATE_QUERY_MARKER',
        ):
            with self.subTest(url=url):
                event = self.event(request={
                    'method': 'POST',
                    'url': url,
                    'headers': ['MALFORMED_PRIVATE_HEADER'],
                })
                self.assertEqual(before_send(event, {}), self.diagnostic())

    def test_known_logs_are_sanitized_without_request_metadata(self):
        for message, category in self.inquiry_logs:
            for fields in (
                {'message': message},
                {'logentry': {'message': message}},
                {'logentry': {'formatted': message}},
            ):
                with self.subTest(message=message, fields=fields):
                    event = self.event(logger='apps.pages.views', **fields)
                    event.pop('request')
                    self.assertEqual(
                        before_send(event, {}), self.diagnostic(category),
                    )

    def test_log_record_hints_protect_events_with_incomplete_metadata(self):
        for message, category in self.inquiry_logs:
            for request in (
                None, [], {}, {'method': ['POST'], 'url': '/'},
                {'method': 'POST', 'url': 'https://[invalid/'},
            ):
                with self.subTest(message=message, request=request):
                    event = self.event(request=request, logentry=[])
                    hint = {'log_record': self.log_record(message)}
                    self.assertEqual(
                        before_send(event, hint), self.diagnostic(category),
                    )

    def test_private_data_is_excluded_without_mutating_event_or_hint(self):
        markers = {
            channel: f'PRIVATE_{channel.upper()}_MARKER'
            for channel in (
                'body', 'url', 'headers', 'user', 'session', 'exception',
                'locals', 'breadcrumbs', 'extra', 'contexts', 'tags',
                'fingerprint', 'attachments', 'message', 'hint', 'unknown',
            )
        }
        event = self.event(
            request={
                'method': 'POST',
                'url': f'https://example.test/?goal={markers["url"]}',
                'data': {'goal': markers['body']},
                'headers': {'Fly-Client-IP': markers['headers']},
                'cookies': {'sessionid': markers['session']},
            },
            user={'ip_address': markers['user'], 'email': markers['user']},
            exception={'values': [{
                'value': markers['exception'],
                'stacktrace': {'frames': [{
                    'vars': {'email_body': markers['locals']},
                }]},
            }]},
            stacktrace={'frames': [{'vars': {'body': markers['locals']}}]},
            threads={'values': [{'stacktrace': {'frames': [{
                'vars': {'body': markers['locals']},
            }]}}]},
            breadcrumbs={'values': [{'message': markers['breadcrumbs']}]},
            extra={'nested': [{'form': markers['extra']}]},
            contexts={'trace': {'data': markers['contexts']}},
            tags={'client': markers['tags']},
            fingerprint=[markers['fingerprint']],
            attachments=[{'data': markers['attachments']}],
            message=markers['message'],
            logentry={'message': markers['message']},
            future_field={'nested': markers['unknown']},
        )
        record = self.log_record(self.inquiry_logs[1][0])
        record.args = (markers['hint'],)
        hint = {
            'log_record': record,
            'request': {'data': markers['hint']},
        }
        original_event = deepcopy(event)
        original_hint_request = deepcopy(hint['request'])
        original_record = deepcopy(record.__dict__)

        result = before_send(event, hint)

        self.assertEqual(result, self.diagnostic('email_delivery'))
        self.assertIsNot(result, event)
        serialized = json.dumps(result)
        for channel, marker in markers.items():
            with self.subTest(channel=channel):
                self.assertNotIn(marker, serialized)
        self.assertEqual(event, original_event)
        self.assertEqual(set(hint), {'log_record', 'request'})
        self.assertEqual(hint['request'], original_hint_request)
        self.assertIs(hint['log_record'], record)
        self.assertEqual(record.__dict__, original_record)

    def test_unrelated_requests_return_the_original_event(self):
        for method, url in (
            ('GET', '/'),
            ('GET', '/?goal=PRIVATE_QUERY_MARKER'),
            ('GET', 'http://[/'),
            ('POST', '/blog/post/'),
            ('POST', '/admin/'),
            ('GET', '/sentry-debug/'),
        ):
            with self.subTest(method=method, url=url):
                event = self.event(
                    request={'method': method, 'url': url},
                    extra={'diagnostic': 'UNRELATED_DATA'},
                )
                original = deepcopy(event)
                self.assertIs(before_send(event, {}), event)
                self.assertEqual(event, original)

    def test_unrelated_logs_are_not_matched_by_message_or_logger_alone(self):
        for logger, message in (
            ('apps.blog.views', self.inquiry_logs[0][0]),
            ('apps.pages.views', 'Unrelated homepage error.'),
        ):
            with self.subTest(logger=logger, message=message):
                event = self.event(
                    logger=logger, logentry={'message': message},
                )
                event.pop('request')
                hint = {'log_record': self.log_record(message, logger)}
                self.assertIs(before_send(event, hint), event)

    def test_malformed_request_metadata_does_not_raise_or_match(self):
        for request in (
            None, [], 'POST /', {},
            {'method': ['POST'], 'url': '/'},
            {'method': 'POST', 'url': ['https://example.test/']},
        ):
            with self.subTest(request=request):
                event = self.event(request=request, logger=[], logentry=[])
                self.assertIs(before_send(event, {'log_record': {}}), event)

    def test_malformed_post_urls_drop_events_without_mutating_inputs(self):
        for url in (
            'http://[/',
            'http://[/?goal=PRIVATE_QUERY_MARKER',
            'https://[invalid/',
            'http://[/blog/',
        ):
            with self.subTest(url=url):
                event = self.event(
                    # Keep URL parsing coverage independent of the Host guard.
                    logger='django.request',
                    request={
                        'method': 'POST',
                        'url': url,
                        'data': {'goal': 'PRIVATE_BRIEF_MARKER'},
                    },
                    extra={'nested': ['PRIVATE_EXTRA_MARKER']},
                )
                hint = {'request': {'data': 'PRIVATE_HINT_MARKER'}}
                original_event = deepcopy(event)
                original_hint = deepcopy(hint)

                self.assertIsNone(before_send(event, hint))
                self.assertEqual(event, original_event)
                self.assertEqual(hint, original_hint)

    def test_disallowed_host_posts_drop_without_trusting_url_or_mutating_inputs(self):
        for method in ('POST', 'post'):
            for url in (
                'http://testserver/blog/',
                'http://testserver?/',
                'http://testserver#/',
                'http://testserver/admin/',
                None,
            ):
                with self.subTest(method=method, url=url):
                    request = {
                        'method': method,
                        'data': {'goal': 'PRIVATE_BRIEF_MARKER'},
                    }
                    if url is not None:
                        request['url'] = url
                    event = self.event(
                        logger='django.security.DisallowedHost',
                        request=request,
                        extra={'nested': ['PRIVATE_EXTRA_MARKER']},
                    )
                    hint = {'request': {'data': 'PRIVATE_HINT_MARKER'}}
                    original_event = deepcopy(event)
                    original_hint = deepcopy(hint)

                    self.assertIsNone(before_send(event, hint))
                    self.assertEqual(event, original_event)
                    self.assertEqual(hint, original_hint)

    def test_host_guard_preserves_gets_and_unrelated_post_loggers(self):
        cases = [
            ('django.security.DisallowedHost', 'GET', url)
            for url in (
                'http://[/', 'http://testserver/blog/',
                'http://testserver?/', 'http://testserver#/',
            )
        ]
        cases.extend(
            (logger, 'POST', url)
            for logger in (
                'django.request', 'apps.blog.views',
                'django.security.DisallowedHost.extra',
            )
            for url in ('http://testserver/blog/', 'http://testserver/admin/')
        )
        for logger, method, url in cases:
            with self.subTest(logger=logger, method=method, url=url):
                event = self.event(
                    logger=logger,
                    request={'method': method, 'url': url},
                    extra={'diagnostic': 'UNRELATED_DATA'},
                )
                hint = {'request': {'data': 'UNRELATED_HINT_DATA'}}
                original_event = deepcopy(event)
                original_hint = deepcopy(hint)

                self.assertIs(before_send(event, hint), event)
                self.assertEqual(event, original_event)
                self.assertEqual(hint, original_hint)

    def test_recognized_events_with_missing_or_invalid_ids_are_dropped(self):
        event = self.event()
        event.pop('event_id')
        self.assertIsNone(before_send(event, {}))
        for event_id in (None, [], 123, 'PRIVATE_ID_MARKER', 'g' * 32):
            with self.subTest(event_id=event_id):
                self.assertIsNone(
                    before_send(self.event(event_id=event_id), {}),
                )

    def test_unsafe_hints_and_attachments_drop_recognized_events(self):
        for hint in (
            [], 'PRIVATE_HINT_MARKER',
            {'attachments': [{'data': 'PRIVATE_ATTACHMENT_MARKER'}]},
            {'attachments': ('PRIVATE_ATTACHMENT_MARKER',)},
            {'attachments': {'data': 'PRIVATE_ATTACHMENT_MARKER'}},
        ):
            with self.subTest(hint=hint):
                event = self.event()
                original_event = deepcopy(event)
                original_hint = deepcopy(hint)
                self.assertIsNone(before_send(event, hint))
                self.assertEqual(event, original_event)
                self.assertEqual(hint, original_hint)

    def test_absent_or_empty_attachments_allow_sanitized_diagnostics(self):
        for hint in (
            None, {}, {'attachments': None}, {'attachments': []},
            {'attachments': ()},
        ):
            with self.subTest(hint=hint):
                self.assertEqual(
                    before_send(self.event(), hint), self.diagnostic(),
                )

    def test_malformed_events_are_dropped_without_raising(self):
        for event in (None, [], 'PRIVATE_EVENT_MARKER'):
            with self.subTest(event=event):
                self.assertIsNone(before_send(event, {}))

    def test_valid_timestamps_are_preserved(self):
        for timestamp in (self.timestamp, '2026-10-09T12:34:56Z'):
            with self.subTest(timestamp=timestamp):
                expected = self.diagnostic()
                expected['timestamp'] = timestamp
                self.assertEqual(
                    before_send(self.event(timestamp=timestamp), {}), expected,
                )

    def test_missing_or_invalid_timestamps_omit_only_that_field(self):
        expected = self.diagnostic()
        expected.pop('timestamp')
        event = self.event()
        event.pop('timestamp')
        self.assertEqual(before_send(event, {}), expected)
        for timestamp in (
            None, [], 123, 'PRIVATE_TIMESTAMP_MARKER',
            '2026-02-30T12:34:56.123456Z',
            '2026-10-09T25:34:56.123456Z',
            '2026-10-09T12:34:56.123456ZPRIVATE_SUFFIX',
        ):
            with self.subTest(timestamp=timestamp):
                self.assertEqual(
                    before_send(self.event(timestamp=timestamp), {}), expected,
                )

    def test_levels_are_preserved_or_default_to_error(self):
        for level in ('debug', 'info', 'warning', 'error', 'critical', 'fatal'):
            with self.subTest(level=level):
                self.assertEqual(
                    before_send(self.event(level=level), {}),
                    self.diagnostic(level=level),
                )
        for level in (None, [], {}, 'PRIVATE_LEVEL_MARKER'):
            with self.subTest(level=level):
                self.assertEqual(
                    before_send(self.event(level=level), {}), self.diagnostic(),
                )


class InquirySentryRegistrationTests(SimpleTestCase):
    def test_application_initialization_registers_privacy_callback(self):
        # An empty test DSN makes get_client() return a NonRecordingClient.
        # Inspect the client actually bound by settings initialization instead.
        client = sentry_sdk.get_global_scope().client
        self.assertIs(client.options['before_send'], before_send)


class InMemorySentryTransport(Transport):
    def __init__(self):
        super().__init__()
        self.envelopes = []
        self.lost_events = []

    def capture_envelope(self, envelope):
        self.envelopes.append(envelope)

    def record_lost_event(self, reason, data_category=None, item=None):
        self.lost_events.append((reason, data_category))


@override_settings(
    DEBUG=False,
    ALLOWED_HOSTS=['testserver'],
    SECURE_SSL_REDIRECT=False,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    PROJECT_INQUIRY_TRUSTED_IP_HEADER='Fly-Client-IP',
    PROJECT_INQUIRY_THROTTLE_LIMIT=1,
    PROJECT_INQUIRY_THROTTLE_WINDOW_SECONDS=60,
)
class InquirySentryTransportTests(TestCase):
    invalid_host_urls = (
        ('[', 'http://[/'),
        ('testserver/blog', 'http://testserver/blog/'),
        ('testserver?', 'http://testserver?/'),
        ('testserver#', 'http://testserver#/'),
    )

    def setUp(self):
        self.transport = InMemorySentryTransport()
        registered_callback = (
            sentry_sdk.get_global_scope().client.options['before_send']
        )
        self.sdk_client = sentry_sdk.Client(
            dsn='https://synthetic@example.test/1',
            transport=self.transport,
            before_send=registered_callback,
            default_integrations=False,
            integrations=[DjangoIntegration(), LoggingIntegration()],
            auto_session_tracking=False,
            traces_sample_rate=0,
            # Exercise the boundary even when enrichment includes private data.
            send_default_pii=True,
            include_local_variables=True,
            max_request_body_size='always',
        )
        self.addCleanup(self.sdk_client.close)
        # SDK 2.18.0 scope copies omit their client. Bind where init() binds,
        # and restore the application client after the request test finishes.
        self.enterContext(patch.object(
            sentry_sdk.get_global_scope(), 'client', self.sdk_client,
        ))
        self.scope = self.enterContext(sentry_sdk.isolation_scope())
        self.scope.clear()
        current_scope = sentry_sdk.get_current_scope()
        current_scope.clear()

        # Silence console handlers while preserving SDK logging capture.
        for name in (
            'apps.pages.views', 'django.request',
            'django.security.DisallowedHost',
        ):
            logger = logging.getLogger(name)
            self.enterContext(patch.object(
                logger, 'handlers', [logging.NullHandler()],
            ))
            self.enterContext(patch.object(logger, 'propagate', False))

        self.markers = {
            channel: f'PRIVATE_{channel.upper()}_MARKER'
            for channel in (
                'name', 'company', 'goal', 'context', 'query', 'header',
                'session', 'exception', 'user', 'breadcrumbs', 'extra',
                'tags', 'fingerprint', 'attachment',
            )
        }
        self.markers['email'] = 'private.email.marker@example.test'
        self.markers['ip'] = '203.0.113.71'
        self.data = {
            'work_area': 'web_application',
            'project_stage': 'building',
            'goal': f'Replace a manual workflow: {self.markers["goal"]}',
            'name': self.markers['name'],
            'email': self.markers['email'],
            'company': self.markers['company'],
            'timing': 'one_to_three_months',
            'additional_context': self.markers['context'],
            'consent': True,
            'website': '',
        }
        self.client = Client(
            HTTP_FLY_CLIENT_IP=self.markers['ip'],
            HTTP_X_PRIVATE_HEADER=self.markers['header'],
            raise_request_exception=False,
        )
        session = self.client.session
        session['private_test_value'] = self.markers['session']
        session.save()
        self.markers['session_cookie'] = self.client.cookies['sessionid'].value
        self.csrf_token = get_token(RequestFactory().get('/'))
        self.client.cookies[settings.CSRF_COOKIE_NAME] = self.csrf_token
        self.url = f'{reverse("home")}?brief={self.markers["query"]}'
        self.scope.set_user({'email': self.markers['user']})
        self.scope.set_extra('nested', {'values': [self.markers['extra']]})
        self.scope.set_context('private', {'value': self.markers['context']})
        self.scope.set_tag('private', self.markers['tags'])
        self.scope.fingerprint = [self.markers['fingerprint']]
        sentry_sdk.add_breadcrumb(message=self.markers['breadcrumbs'])

    def request(self, method='post', **headers):
        # Django's test Client bypasses WSGIHandler.__call__, where the SDK
        # installs method/URL enrichment. Exercise that production boundary.
        request_headers = {
            'HTTP_FLY_CLIENT_IP': self.markers['ip'],
            'HTTP_X_PRIVATE_HEADER': self.markers['header'],
            'HTTP_X_CSRFTOKEN': self.csrf_token,
            'HTTP_COOKIE': self.client.cookies.output(
                header='', sep=';',
            ).strip(),
        }
        request_headers.update(headers)
        request = getattr(RequestFactory(), method)(
            self.url,
            data=self.data if method == 'post' else None,
            **request_headers,
        )
        statuses = []

        def start_response(status, response_headers):
            statuses.append(int(status.split()[0]))

        response = WSGIHandler()(request.META, start_response)
        try:
            b''.join(response)
        finally:
            response.close()
        return statuses[0]

    def assert_private_diagnostic(self, category):
        self.assertEqual(len(self.transport.envelopes), 1)
        envelope = self.transport.envelopes[0]
        self.assertEqual([item.type for item in envelope.items], ['event'])
        # Decode the final wire representation, rather than a callback result.
        serialized = envelope.serialize()
        lines = serialized.splitlines()
        event = json.loads(lines[2])
        self.assertEqual(set(event), {
            'event_id', 'timestamp', 'level', 'message', 'tags', 'fingerprint',
        })
        self.assertRegex(event['event_id'], r'^[0-9a-f]{32}$')
        self.assertEqual(json.loads(lines[0])['event_id'], event['event_id'])
        self.assertRegex(event['timestamp'], r'^\d{4}-\d{2}-\d{2}T.+Z$')
        self.assertEqual(event['level'], 'error')
        self.assertEqual(event['message'], 'Project inquiry failed.')
        self.assertEqual(event['tags'], {'project_inquiry_failure': category})
        self.assertEqual(event['fingerprint'], ['project-inquiry', category])
        for channel, marker in self.markers.items():
            with self.subTest(channel=channel):
                self.assertNotIn(marker.encode(), serialized)

    def test_throttle_failures_reach_transport_as_private_diagnostics(self):
        for error in (
            ProjectInquiryThrottleError(self.markers['exception']),
            DatabaseError(self.markers['exception']),
        ):
            with self.subTest(error=type(error).__name__):
                self.transport.envelopes.clear()
                with patch(
                    'apps.pages.views.consume_project_inquiry_throttle',
                    side_effect=error,
                ):
                    status = self.request()
                self.assertEqual(status, 200)
                self.assert_private_diagnostic('throttle')

        # Run the actual malformed-header branch, without mocking the throttle.
        self.transport.envelopes.clear()
        malformed_header = '203.0.113.71, 203.0.113.72'
        self.markers['malformed_header'] = malformed_header
        status = self.request(HTTP_FLY_CLIENT_IP=malformed_header)
        self.assertEqual(status, 200)
        self.assert_private_diagnostic('throttle')

    def test_smtp_failure_reaches_transport_as_private_diagnostic(self):
        with patch(
            'apps.pages.views.EmailMessage.send',
            side_effect=RuntimeError(self.markers['exception']),
        ) as send:
            status = self.request()
        self.assertEqual(status, 200)
        send.assert_called_once_with(fail_silently=False)
        self.assert_private_diagnostic('email_delivery')

    def test_unexpected_post_root_error_is_sanitized_by_django_capture(self):
        # This exception is outside the two logger.exception branches.
        with patch(
            'apps.pages.views.render_to_string',
            side_effect=RuntimeError(self.markers['exception']),
        ):
            status = self.request()
        self.assertEqual(status, 500)
        self.assert_private_diagnostic('other')

    def test_invalid_host_posts_drop_private_events_before_transport(self):
        self.url = reverse('home')
        for send_default_pii in (False, True):
            for host, sdk_url in self.invalid_host_urls:
                with self.subTest(host=host, send_default_pii=send_default_pii):
                    self.transport.envelopes.clear()
                    self.transport.lost_events.clear()
                    callback = Mock(wraps=self.sdk_client.options['before_send'])
                    with patch.dict(self.sdk_client.options, {
                        'send_default_pii': send_default_pii,
                        'before_send': callback,
                    }):
                        status = self.request(HTTP_HOST=host)

                    self.assertEqual(status, 400)
                    callback.assert_called_once()
                    event = callback.call_args.args[0]
                    self.assertEqual(
                        event['logger'], 'django.security.DisallowedHost',
                    )
                    self.assertEqual(event['request']['method'], 'POST')
                    self.assertEqual(event['request']['url'], sdk_url)
                    self.assertIn(
                        self.markers['goal'], event['request']['data']['goal'],
                    )
                    self.assertEqual(self.transport.envelopes, [])
                    self.assertIn(
                        ('before_send', 'error'), self.transport.lost_events,
                    )

    def test_invalid_host_gets_keep_normal_diagnostics(self):
        self.url = reverse('home')
        for host, sdk_url in self.invalid_host_urls:
            with self.subTest(host=host):
                self.transport.envelopes.clear()
                self.transport.lost_events.clear()
                status = self.request(method='get', HTTP_HOST=host)

                self.assertEqual(status, 400)
                self.assertEqual(len(self.transport.envelopes), 1)
                serialized = self.transport.envelopes[0].serialize()
                event = json.loads(serialized.splitlines()[2])
                self.assertEqual(
                    event['logger'], 'django.security.DisallowedHost',
                )
                self.assertEqual(event['request']['method'], 'GET')
                self.assertEqual(event['request']['url'], sdk_url)
                exception = event['exception']['values'][-1]
                self.assertEqual(exception['type'], 'DisallowedHost')
                self.assertIn(host, exception['value'])
                self.assertEqual(event['extra']['nested'], {
                    'values': [self.markers['extra']],
                })
                self.assertNotIn(
                    ('before_send', 'error'), self.transport.lost_events,
                )

    def test_unrelated_home_get_error_keeps_normal_diagnostics(self):
        with patch(
            'apps.pages.views.HomePageView.get_context_data',
            side_effect=RuntimeError('UNRELATED_EXCEPTION_MARKER'),
        ):
            status = self.request(method='get')
        self.assertEqual(status, 500)
        self.assertEqual(len(self.transport.envelopes), 1)
        event = self.transport.envelopes[0].get_event()
        self.assertEqual(event['request']['method'], 'GET')
        self.assertEqual(
            event['exception']['values'][0]['value'],
            'UNRELATED_EXCEPTION_MARKER',
        )
        self.assertEqual(event['extra']['nested'], {
            'values': [self.markers['extra']],
        })
        self.assertIn(
            b'UNRELATED_EXCEPTION_MARKER',
            self.transport.envelopes[0].serialize(),
        )

    def test_inquiry_attachment_drops_entire_outgoing_envelope(self):
        self.scope.add_attachment(
            bytes=self.markers['attachment'].encode(),
            filename='synthetic-private.txt',
        )
        with patch(
            'apps.pages.views.consume_project_inquiry_throttle',
            side_effect=RuntimeError(self.markers['exception']),
        ):
            status = self.request()
        self.assertEqual(status, 200)
        self.assertEqual(self.transport.envelopes, [])
        self.assertIn(('before_send', 'error'), self.transport.lost_events)
