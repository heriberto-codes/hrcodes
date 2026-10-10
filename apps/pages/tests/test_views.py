from datetime import datetime, timedelta, timezone as datetime_timezone
from html.parser import HTMLParser
from pathlib import Path
from unittest.mock import patch

from django.contrib.messages import get_messages
from django.contrib.staticfiles import finders
from django.core import mail
from django.db import DatabaseError
from django.template import engines
from django.test import Client, TestCase, override_settings
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse

from apps.blog.models import Category, Post
from apps.pages.forms import ProjectBriefForm
from apps.pages.models import ProjectInquiryThrottle
from apps.pages.throttling import ProjectInquiryThrottleError
from apps.pages.views import (
    PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
    PROJECT_INQUIRY_DELIVERY_ERROR,
)


class HomepageLandmarkParser(HTMLParser):
    section_ids = {
        'hero',
        'services',
        'proof',
        'process',
        'insights',
        'about',
        'start-a-project',
    }

    def __init__(self):
        super().__init__()
        self.landmarks = []
        self.main_depth = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'main':
            self.main_depth += 1
        elif tag == 'section' and attributes.get('id') in self.section_ids:
            self.landmarks.append(attributes['id'])
        elif tag == 'footer' and self.main_depth == 0:
            self.landmarks.append('footer')

    def handle_endtag(self, tag):
        if tag == 'main' and self.main_depth:
            self.main_depth -= 1


class HomepageContinuityParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.fragment_targets = []
        self.heading_one_count = 0
        self.ids = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        element_id = attributes.get('id')
        href = attributes.get('href', '')

        if element_id:
            self.ids.append(element_id)
        if tag == 'a' and href.startswith('#') and len(href) > 1:
            self.fragment_targets.append(href[1:])
        if tag == 'h1':
            self.heading_one_count += 1


@override_settings(
    DEBUG=False,
    EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
    DEFAULT_FROM_EMAIL='Hroman Codes <no-reply@example.com>',
    PROJECT_INQUIRY_RECIPIENT='inquiries@example.com',
    PROJECT_INQUIRY_COOLDOWN_SECONDS=60,
    PROJECT_INQUIRY_TRUSTED_IP_HEADER='Fly-Client-IP',
    PROJECT_INQUIRY_THROTTLE_LIMIT=1,
    PROJECT_INQUIRY_THROTTLE_WINDOW_SECONDS=60,
)
class TestViews(TestCase):
    INSIGHT_SLUGS = (
        "i-revived-my-reactredux-app-with-turtle-ai-and-learned-where-ai-"
        "guardrails-can-go-too-far",
        "how-constraints-changed-the-way-i-think-about-algorithms",
        "i-revived-a-9-year-old-app-with-openai-codex-with-a-product-"
        "engineer-mindset",
    )
    INSIGHT_NAMES = ("Guardrails", "Constraints", "Revival")

    def setUp(self):
        self.client = Client(HTTP_FLY_CLIENT_IP='203.0.113.20')
        self.base_url = reverse('home')
        self.now = datetime(
            2026, 1, 1, 12, 0, 59, tzinfo=datetime_timezone.utc,
        )
        clock_patch = patch(
            'apps.pages.throttling.timezone.now',
            return_value=self.now,
        )
        self.throttle_clock = clock_patch.start()
        self.addCleanup(clock_patch.stop)

    def create_insight_post(self, index, status=1):
        post = Post.objects.create(
            title=f"Insight {index + 1}",
            slug=self.INSIGHT_SLUGS[index],
            snippet=f"Insight snippet {index + 1}",
            status=status,
        )
        category = Category.objects.create(
            name=f"Topic {index + 1}",
            slug=f"topic-{index + 1}",
        )
        post.categories.add(category)
        return post

    def project_brief_data(self, **overrides):
        data = {
            'work_area': 'web_application',
            'project_stage': 'building',
            'goal': 'Replace a manual intake workflow with a useful product.',
            'name': 'Ada Lovelace',
            'email': 'ADA@EXAMPLE.COM',
            'company': 'Analytical Engines',
            'timing': 'one_to_three_months',
            'additional_context': 'The current process uses spreadsheets.',
            'consent': True,
            'website': '',
        }
        data.update(overrides)
        return data

    def test_can_load_base_template(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
    
    def test_can_view_home_template(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_get_exposes_unbound_project_brief_form(self):
        response = self.client.get(self.base_url)

        form = response.context['form']
        self.assertIsInstance(form, ProjectBriefForm)
        self.assertFalse(form.is_bound)

    def test_home_renders_start_project_brief_contract(self):
        response = self.client.get(self.base_url)
        content = response.content.decode()

        self.assertIn('id="start-a-project"', content)
        self.assertIn('class="home-start-project"', content)
        self.assertIn('data-home-project', content)
        self.assertIn('class="home-builder-form"', content)
        self.assertIn('method="post"', content)
        self.assertIn('action="#start-a-project"', content)
        self.assertIn('data-home-project-form', content)
        self.assertIn('name="csrfmiddlewaretoken"', content)
        self.assertEqual(content.count('data-home-step="'), 3)
        self.assertIn('data-home-project-progress', content)
        self.assertIn('data-home-summary="area"', content)
        self.assertIn('data-home-summary="stage"', content)
        self.assertIn('data-home-summary="goal"', content)

        for field_name in (
            'work_area',
            'project_stage',
            'goal',
            'name',
            'email',
            'company',
            'timing',
            'additional_context',
            'consent',
            'website',
        ):
            self.assertIn(f'name="{field_name}"', content)

        for step_number in ('1', '2', '3'):
            self.assertNotRegex(
                content,
                rf'<section[^>]+data-home-step="{step_number}"[^>]+hidden',
            )

        self.assertIn(
            'href="https://calendly.com/heriberto_codes/coffee_chat" '
            'target="_blank" rel="noopener noreferrer"',
            content,
        )
        self.assertNotIn('data-home-project-success', content)

    def test_valid_project_brief_sends_email_and_redirects(self):
        response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
        )

        self.assertRedirects(
            response,
            f'{self.base_url}#start-a-project',
            fetch_redirect_response=False,
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(ProjectInquiryThrottle.objects.get().attempt_count, 1)
        message = mail.outbox[0]
        self.assertEqual(message.subject, 'New Hroman Codes project brief')
        self.assertEqual(
            message.from_email,
            'Hroman Codes <no-reply@example.com>',
        )
        self.assertEqual(message.to, ['inquiries@example.com'])
        self.assertEqual(message.reply_to, ['ada@example.com'])
        for body_text in (
            'Name: Ada Lovelace',
            'Email: ada@example.com',
            'Company: Analytical Engines',
            'Work area: Custom Web Applications',
            'Project stage: Building now',
            'Timing: Within 1–3 months',
            'Replace a manual intake workflow with a useful product.',
            'The current process uses spreadsheets.',
        ):
            self.assertIn(body_text, message.body)

        self.assertIn(
            PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
            self.client.session,
        )
        self.assertIn(
            'Your project brief was sent. Thank you for the context.',
            [str(message) for message in get_messages(response.wsgi_request)],
        )

    def test_invalid_project_brief_preserves_data_without_side_effects(self):
        response = self.client.post(
            self.base_url,
            data=self.project_brief_data(goal='Too short'),
        )

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.is_bound)
        self.assertIn('goal', form.errors)
        self.assertEqual(form.data['name'], 'Ada Lovelace')
        self.assertEqual(form.data['goal'], 'Too short')
        self.assertContains(response, 'data-initial-step="2"')
        self.assertContains(response, form.errors['goal'][0])
        self.assertContains(
            response,
            'name="goal" placeholder="Describe the change you want for '
            'the business, team, or people using the product." required '
            'minlength="20" maxlength="2000" '
            'aria-describedby="home-project-goal-help '
            'home-project-goal-error" aria-invalid="true">Too short',
        )
        self.assertEqual(mail.outbox, [])
        self.assertNotIn(
            PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
            self.client.session,
        )
        self.assertEqual(list(get_messages(response.wsgi_request)), [])
        self.assertFalse(ProjectInquiryThrottle.objects.exists())

    @patch(
        'apps.pages.views.EmailMessage.send',
        side_effect=RuntimeError('SMTP unavailable'),
    )
    def test_delivery_exception_rerenders_bound_form_safely(self, send):
        with self.assertLogs('apps.pages.views', level='ERROR'):
            response = self.client.post(
                self.base_url,
                data=self.project_brief_data(),
            )

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.data['name'], 'Ada Lovelace')
        self.assertIn(PROJECT_INQUIRY_DELIVERY_ERROR, form.non_field_errors())
        self.assertContains(response, 'data-initial-step="3"')
        self.assertContains(response, 'data-home-form-wide-error')
        self.assertContains(response, PROJECT_INQUIRY_DELIVERY_ERROR)
        self.assertNotContains(response, 'data-home-project-success')
        send.assert_called_once_with(fail_silently=False)
        self.assertEqual(mail.outbox, [])
        self.assertNotIn(
            PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
            self.client.session,
        )
        self.assertEqual(list(get_messages(response.wsgi_request)), [])
        self.assertEqual(ProjectInquiryThrottle.objects.get().attempt_count, 1)

        retry_response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
        )

        self.assertEqual(retry_response.status_code, 200)
        self.assertIn(
            'Please wait a moment before sending another project brief.',
            retry_response.context['form'].non_field_errors(),
        )
        send.assert_called_once_with(fail_silently=False)
        self.assertEqual(mail.outbox, [])
        self.assertNotIn(
            PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
            self.client.session,
        )
        self.assertEqual(ProjectInquiryThrottle.objects.get().attempt_count, 1)

    @patch('apps.pages.views.EmailMessage.send', return_value=0)
    def test_zero_delivery_rerenders_bound_form_safely(self, send):
        response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
        )

        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertEqual(form.data['goal'], self.project_brief_data()['goal'])
        self.assertIn(PROJECT_INQUIRY_DELIVERY_ERROR, form.non_field_errors())
        send.assert_called_once_with(fail_silently=False)
        self.assertEqual(mail.outbox, [])
        self.assertNotIn(
            PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
            self.client.session,
        )
        self.assertEqual(ProjectInquiryThrottle.objects.get().attempt_count, 1)

        retry_response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
        )

        self.assertEqual(retry_response.status_code, 200)
        self.assertIn(
            'Please wait a moment before sending another project brief.',
            retry_response.context['form'].non_field_errors(),
        )
        send.assert_called_once_with(fail_silently=False)
        self.assertEqual(mail.outbox, [])
        self.assertNotIn(
            PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
            self.client.session,
        )
        self.assertEqual(ProjectInquiryThrottle.objects.get().attempt_count, 1)

    def test_recent_successful_submission_blocks_duplicate_email(self):
        first_response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
        )
        sent_at = self.client.session[
            PROJECT_INQUIRY_COOLDOWN_SESSION_KEY
        ]
        confirmation_response = self.client.get(first_response.url)
        self.assertContains(confirmation_response, 'data-home-project-success')

        second_response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
        )

        self.assertEqual(first_response.status_code, 302)
        self.assertEqual(second_response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            self.client.session[PROJECT_INQUIRY_COOLDOWN_SESSION_KEY],
            sent_at,
        )
        self.assertIn(
            'Please wait a moment before sending another project brief.',
            second_response.context['form'].non_field_errors(),
        )
        self.assertEqual(
            second_response.context['form'].data['goal'],
            self.project_brief_data()['goal'],
        )
        self.assertContains(second_response, 'data-initial-step="3"')
        self.assertContains(second_response, 'data-home-form-wide-error')
        self.assertContains(
            second_response,
            'https://calendly.com/heriberto_codes/coffee_chat',
        )
        self.assertNotContains(second_response, 'data-home-project-success')
        self.assertEqual(
            list(get_messages(second_response.wsgi_request)), [],
        )
        self.assertEqual(ProjectInquiryThrottle.objects.get().attempt_count, 1)

    def test_fresh_sessions_share_throttle_only_for_same_client_address(self):
        first_response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
        )
        fresh_client = Client(HTTP_FLY_CLIENT_IP='203.0.113.20')
        changed_brief = self.project_brief_data(
            email='grace@example.com',
            goal='Build a different product for a different business.',
        )

        blocked_response = fresh_client.post(
            self.base_url,
            data=changed_brief,
        )

        self.assertEqual(first_response.status_code, 302)
        self.assertEqual(blocked_response.status_code, 200)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            'Please wait a moment before sending another project brief.',
            blocked_response.context['form'].non_field_errors(),
        )
        self.assertEqual(
            blocked_response.context['form'].data['goal'],
            changed_brief['goal'],
        )
        self.assertNotIn(
            PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
            fresh_client.session,
        )
        self.assertEqual(ProjectInquiryThrottle.objects.get().attempt_count, 1)

        different_client = Client(HTTP_FLY_CLIENT_IP='203.0.113.21')
        allowed_response = different_client.post(
            self.base_url,
            data=changed_brief,
        )

        self.assertRedirects(
            allowed_response,
            f'{self.base_url}#start-a-project',
            fetch_redirect_response=False,
        )
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(ProjectInquiryThrottle.objects.count(), 2)

    def test_fresh_sessions_cannot_bypass_limit_by_changing_forwarded_for(self):
        first_response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
            HTTP_X_FORWARDED_FOR='198.51.100.8',
        )
        self.assertEqual(first_response.status_code, 302)

        for forwarded_for in (
            '198.51.100.9',
            '198.51.100.10, 198.51.100.11',
        ):
            with self.subTest(forwarded_for=forwarded_for):
                fresh_client = Client(HTTP_FLY_CLIENT_IP='203.0.113.20')
                response = fresh_client.post(
                    self.base_url,
                    data=self.project_brief_data(),
                    HTTP_X_FORWARDED_FOR=forwarded_for,
                )

                self.assertEqual(response.status_code, 200)
                self.assertIn(
                    'Please wait a moment before sending another project brief.',
                    response.context['form'].non_field_errors(),
                )
                self.assertEqual(len(mail.outbox), 1)
                self.assertNotIn(
                    PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
                    fresh_client.session,
                )
                self.assertEqual(
                    ProjectInquiryThrottle.objects.get().attempt_count, 1,
                )

    def test_trusted_header_list_fails_closed_without_email_or_bucket(self):
        trusted_header = '203.0.113.20, 203.0.113.21'
        with self.assertLogs('apps.pages.views', level='ERROR'):
            with patch('apps.pages.views.EmailMessage.send') as send:
                response = self.client.post(
                    self.base_url,
                    data=self.project_brief_data(),
                    HTTP_FLY_CLIENT_IP=trusted_header,
                    HTTP_X_FORWARDED_FOR='198.51.100.8',
                )

        send.assert_not_called()
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        self.assertTrue(form.is_bound)
        for field, value in self.project_brief_data().items():
            self.assertEqual(form.data[field], str(value))
        self.assertEqual(
            list(form.non_field_errors()), [PROJECT_INQUIRY_DELIVERY_ERROR],
        )
        self.assertContains(response, PROJECT_INQUIRY_DELIVERY_ERROR)
        self.assertContains(response, 'data-initial-step="3"')
        self.assertContains(response, 'data-home-form-wide-error')
        self.assertContains(
            response, 'https://calendly.com/heriberto_codes/coffee_chat',
        )
        self.assertNotContains(response, trusted_header)
        self.assertNotContains(response, '198.51.100.8')
        self.assertNotContains(response, 'data-home-project-success')
        self.assertEqual(mail.outbox, [])
        self.assertFalse(ProjectInquiryThrottle.objects.exists())
        self.assertNotIn(
            PROJECT_INQUIRY_COOLDOWN_SESSION_KEY, self.client.session,
        )
        self.assertEqual(list(get_messages(response.wsgi_request)), [])

    def test_new_window_allows_submission_despite_recent_session_timestamp(self):
        first_response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
        )
        self.assertEqual(first_response.status_code, 302)
        sent_at = self.client.session[PROJECT_INQUIRY_COOLDOWN_SESSION_KEY]
        first_key = ProjectInquiryThrottle.objects.get().bucket_key
        self.throttle_clock.return_value = self.now + timedelta(seconds=1)

        self.assertEqual(
            self.throttle_clock.return_value.timestamp() - sent_at, 1,
        )
        response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
        )

        self.assertRedirects(
            response,
            f'{self.base_url}#start-a-project',
            fetch_redirect_response=False,
        )
        self.assertEqual(len(mail.outbox), 2)
        bucket = ProjectInquiryThrottle.objects.get()
        self.assertNotEqual(bucket.bucket_key, first_key)
        self.assertEqual(bucket.attempt_count, 1)

    def test_throttle_errors_fail_closed_with_generic_bound_form_feedback(self):
        errors = (
            ProjectInquiryThrottleError('Throttle configuration unavailable'),
            DatabaseError('Throttle database unavailable'),
        )
        for error in errors:
            with self.subTest(error=type(error).__name__):
                with patch(
                    'apps.pages.views.consume_project_inquiry_throttle',
                    side_effect=error,
                ) as consume, patch(
                    'apps.pages.views.EmailMessage.send',
                ) as send, self.assertLogs(
                    'apps.pages.views', level='ERROR',
                ) as logs:
                    response = self.client.post(
                        self.base_url,
                        data=self.project_brief_data(),
                    )

                consume.assert_called_once()
                self.assertIs(consume.call_args.args[0], response.wsgi_request)
                send.assert_not_called()
                self.assertEqual(response.status_code, 200)
                form = response.context['form']
                self.assertTrue(form.is_bound)
                self.assertEqual(form.data['name'], 'Ada Lovelace')
                self.assertEqual(
                    form.data['goal'], self.project_brief_data()['goal'],
                )
                self.assertEqual(
                    list(form.non_field_errors()),
                    [PROJECT_INQUIRY_DELIVERY_ERROR],
                )
                self.assertContains(response, PROJECT_INQUIRY_DELIVERY_ERROR)
                self.assertContains(response, 'data-initial-step="3"')
                self.assertContains(response, 'data-home-form-wide-error')
                self.assertContains(
                    response,
                    'https://calendly.com/heriberto_codes/coffee_chat',
                )
                self.assertNotContains(response, str(error))
                self.assertNotContains(response, '203.0.113.20')
                self.assertNotContains(response, 'data-home-project-success')
                self.assertEqual(mail.outbox, [])
                self.assertEqual(list(get_messages(response.wsgi_request)), [])
                self.assertNotIn(
                    PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
                    self.client.session,
                )
                self.assertFalse(ProjectInquiryThrottle.objects.exists())
                self.assertEqual(
                    logs.records[0].getMessage(),
                    'Project inquiry throttle evaluation failed.',
                )
                self.assertIsNotNone(logs.records[0].exc_info)

    def test_honeypot_rejects_submission_without_consuming_throttle(self):
        with patch(
            'apps.pages.views.consume_project_inquiry_throttle',
        ) as consume:
            response = self.client.post(
                self.base_url,
                data=self.project_brief_data(website='https://spam.example'),
            )

        consume.assert_not_called()
        self.assertEqual(response.status_code, 200)
        self.assertIn('website', response.context['form'].errors)
        self.assertEqual(mail.outbox, [])
        self.assertFalse(ProjectInquiryThrottle.objects.exists())
        self.assertNotIn(
            PROJECT_INQUIRY_COOLDOWN_SESSION_KEY,
            self.client.session,
        )

    def test_corrupt_cooldown_timestamp_does_not_block_submission(self):
        session = self.client.session
        session[PROJECT_INQUIRY_COOLDOWN_SESSION_KEY] = 'not-a-timestamp'
        session.save()

        response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(mail.outbox), 1)
        self.assertIsInstance(
            self.client.session[PROJECT_INQUIRY_COOLDOWN_SESSION_KEY],
            float,
        )

    def test_project_brief_post_requires_csrf_token(self):
        csrf_client = Client(
            enforce_csrf_checks=True,
            HTTP_FLY_CLIENT_IP='203.0.113.20',
        )

        response = csrf_client.post(
            self.base_url,
            data=self.project_brief_data(),
        )

        self.assertEqual(response.status_code, 403)
        self.assertEqual(mail.outbox, [])
        self.assertFalse(ProjectInquiryThrottle.objects.exists())

    def test_successful_project_brief_renders_confirmation_after_redirect(self):
        response = self.client.post(
            self.base_url,
            data=self.project_brief_data(),
            follow=True,
        )

        self.assertEqual(
            response.redirect_chain,
            [(f'{self.base_url}#start-a-project', 302)],
        )
        self.assertContains(response, 'data-home-project-success')
        self.assertContains(response, 'data-home-reset-project')
        self.assertContains(
            response,
            'Your project brief was sent. Thank you for the context.',
        )
        self.assertContains(response, 'data-home-project-form')
        self.assertEqual(len(mail.outbox), 1)

    def test_home_renders_complete_insights_tuner_in_approved_order(self):
        posts_by_slug = {}
        for index in reversed(range(len(self.INSIGHT_SLUGS))):
            post = self.create_insight_post(index)
            posts_by_slug[post.slug] = post

        response = self.client.get(self.base_url)
        insight_signals = response.context['insight_signals']

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            [signal['post'].slug for signal in insight_signals],
            list(self.INSIGHT_SLUGS),
        )
        self.assertEqual(
            [signal['name'] for signal in insight_signals],
            list(self.INSIGHT_NAMES),
        )
        self.assertEqual(
            [post.slug for post in response.context['posts']],
            list(self.INSIGHT_SLUGS),
        )
        self.assertEqual(response.context['insight_signal_count'], 3)
        self.assertTrue(response.context['insights_complete'])
        self.assertEqual(response.context['missing_insight_channels'], [])

        for index, signal in enumerate(insight_signals):
            post = posts_by_slug[signal['post'].slug]
            self.assertIn(
                'categories',
                signal['post']._prefetched_objects_cache,
            )
            self.assertContains(response, post.title)
            self.assertContains(response, post.snippet)
            self.assertContains(response, f"Topic {index + 1}")
            self.assertContains(
                response,
                reverse(
                    'blog_detail',
                    kwargs={'pk': post.pk, 'slug': post.slug},
                ),
            )

        self.assertContains(
            response,
            'name="home-insight-signal"',
            count=3,
        )
        self.assertContains(response, '03 signals loaded')
        self.assertContains(response, 'Open all Insights')
        self.assertContains(response, reverse('blog_index'))
        self.assertNotContains(
            response,
            'Some selected notes are temporarily off air.',
        )
        self.assertNotContains(
            response,
            'No signals are broadcasting right now.',
        )

    def test_home_renders_partial_insights_tuner_with_off_air_state(self):
        available_third = self.create_insight_post(2)
        available_first = self.create_insight_post(0)
        draft = self.create_insight_post(1, status=0)
        unrelated = Post.objects.create(
            title='Unrelated published note',
            slug='unrelated-published-note',
            snippet='This note is not an approved Insights channel.',
            status=1,
        )

        response = self.client.get(self.base_url)
        insight_signals = response.context['insight_signals']

        self.assertEqual(
            [signal['post'].slug for signal in insight_signals],
            [available_first.slug, available_third.slug],
        )
        self.assertEqual(
            [signal['name'] for signal in insight_signals],
            ['Guardrails', 'Revival'],
        )
        self.assertEqual(response.context['insight_signal_count'], 2)
        self.assertFalse(response.context['insights_complete'])
        self.assertEqual(
            response.context['missing_insight_channels'],
            ['Constraints'],
        )
        self.assertContains(response, available_first.title)
        self.assertContains(response, available_third.title)
        self.assertNotContains(response, draft.title)
        self.assertNotContains(response, unrelated.title)
        self.assertContains(
            response,
            'name="home-insight-signal"',
            count=2,
        )
        self.assertContains(response, '02 signals loaded')
        self.assertContains(
            response,
            'Some selected notes are temporarily off air.',
        )
        self.assertNotContains(
            response,
            'No signals are broadcasting right now.',
        )

    def test_home_renders_empty_insights_fallback_without_tuner_controls(self):
        draft = self.create_insight_post(0, status=0)
        unrelated = Post.objects.create(
            title='Another published note',
            slug='another-published-note',
            snippet='This note is not an approved Insights channel.',
            status=1,
        )

        response = self.client.get(self.base_url)

        self.assertEqual(response.context['insight_signals'], [])
        self.assertEqual(response.context['posts'], [])
        self.assertEqual(response.context['insight_signal_count'], 0)
        self.assertFalse(response.context['insights_complete'])
        self.assertEqual(
            response.context['missing_insight_channels'],
            list(self.INSIGHT_NAMES),
        )
        self.assertNotContains(response, draft.title)
        self.assertNotContains(response, unrelated.title)
        self.assertNotContains(response, 'name="home-insight-signal"')
        self.assertNotContains(response, 'class="home-insight-selector"')
        self.assertContains(
            response,
            'No signals are broadcasting right now.',
        )
        self.assertContains(response, 'Open the Insights archive')
        self.assertContains(response, reverse('blog_index'))

    def test_home_insights_css_preserves_tuner_accessibility_and_layout(self):
        home_css_path = finders.find('pages/home.css')
        css = Path(home_css_path).read_text(encoding='utf-8')

        self.assertIn(
            '.home-page #home-signal-1:focus-visible '
            '~ .home-insight-tabs',
            css,
        )
        self.assertIn(
            '.home-page .home-insight-story:first-child { display: grid;',
            css,
        )
        self.assertIn(
            '.home-page .home-insight-selector:'
            'has(#home-signal-2:checked) .home-insight-story-2',
            css,
        )
        self.assertIn('@media (max-width: 1080px)', css)
        self.assertIn('@media (max-width: 760px)', css)
        self.assertIn('@media (max-width: 460px)', css)
        self.assertIn(
            '.home-page .home-insight-tabs { border-bottom:',
            css,
        )
        self.assertIn('@media (prefers-reduced-motion: reduce)', css)
        self.assertIn(
            '.home-page .home-insight-wave i { animation: none; }',
            css,
        )

    def test_home_uses_page_scoped_foundation(self):
        response = self.client.get(self.base_url)
        home_css_path = finders.find('pages/home.css')
        home_js_path = finders.find('pages/home.js')

        self.assertContains(
            response,
            '<title>Software Development for Growing Businesses | '
            'Hroman Codes</title>',
            html=True,
        )
        self.assertContains(
            response,
            '<meta name="description" content="Hroman Codes turns business '
            'problems into reliable digital products, practical automation, '
            'and scalable software.">',
            html=True,
        )
        self.assertContains(
            response,
            '<body class="hrBody home-page">',
        )
        self.assertContains(
            response,
            f'href="{static("pages/home.css")}?v=20260926-continuity-4"',
        )
        self.assertContains(
            response,
            f'<script src="{static("pages/home.js")}'
            '?v=20260926-continuity-3" defer></script>',
            html=True,
        )
        self.assertIsNotNone(home_css_path)
        self.assertIsNotNone(home_js_path)

    def test_home_renders_approved_native_navigation_contract(self):
        navbar = render_to_string('includes/navbar.html')
        nav_targets = (
            '#services',
            '#proof',
            '#process',
            '#insights',
            '#about',
            '#start-a-project',
        )

        self.assertIn(
            '<a class="home-skip-link" href="#main-content">'
            'Skip to main content</a>',
            navbar,
        )
        self.assertIn(
            '<nav class="home-desktop-nav" aria-label="Primary navigation">',
            navbar,
        )
        self.assertIn(
            '<details class="home-mobile-nav" data-home-mobile-nav>',
            navbar,
        )
        self.assertIn('<summary aria-label="Open navigation">', navbar)
        self.assertIn('<nav aria-label="Mobile navigation">', navbar)
        self.assertNotIn(
            '<details class="home-mobile-nav" data-home-mobile-nav open>',
            navbar,
        )

        for target in nav_targets:
            self.assertEqual(navbar.count(f'href="{target}"'), 2)

    def test_home_renders_hero_c_semantic_fallbacks_and_routes(self):
        hero = render_to_string('includes/hero.html')
        working_photo_path = finders.find(
            'pages/images/heriberto-working.jpg'
        )

        self.assertIn(
            '<section class="home-hero" id="hero" '
            'aria-labelledby="hero-title">',
            hero,
        )
        self.assertIn('<h1 id="hero-title">', hero)
        self.assertIn(
            '<span class="home-pixel-word-text">software</span>',
            hero,
        )
        self.assertIn(
            '<canvas class="home-pixel-word-canvas" '
            'aria-hidden="true"></canvas>',
            hero,
        )
        self.assertIn(
            '<img class="home-mosaic-source" '
            f'src="{static("pages/images/heriberto-working.jpg")}" '
            'alt="Heriberto Roman working at a laptop and external monitor">',
            hero,
        )
        self.assertIn(
            '<div class="home-mosaic-grid" aria-hidden="true">',
            hero,
        )
        self.assertEqual(hero.count('<span></span>'), 9)
        self.assertIn('Your partner in the work', hero)
        self.assertIn('Accepting select projects', hero)
        self.assertIn(
            'href="https://calendly.com/heriberto_codes/coffee_chat" '
            'target="_blank" rel="noopener noreferrer"',
            hero,
        )
        self.assertIn('href="#services">Review Services</a>', hero)
        self.assertIsNotNone(working_photo_path)

    def test_home_renders_services_b_contract(self):
        services = render_to_string('includes/services.html')
        service_names = (
            'MVP &amp; Product Development',
            'Custom Web Applications',
            'UX/UI Design &amp; Prototyping',
            'AI &amp; Workflow Automation',
            'Maintenance &amp; Technical Support',
        )

        self.assertIn(
            '<section id="services" class="home-services" '
            'aria-labelledby="services-title">',
            services,
        )
        self.assertIn('<h2 id="services-title">', services)
        self.assertNotIn('<h1', services)
        self.assertEqual(
            services.count('class="home-service-row'),
            5,
        )
        self.assertEqual(
            services.count('home-service-row-featured'),
            1,
        )
        self.assertEqual(
            services.count('<span>Typical deliverables</span>'),
            5,
        )
        self.assertEqual(
            services.count(
                'class="home-service-fit-link" '
                'href="#service-project-fit"'
            ),
            5,
        )
        self.assertEqual(
            services.count(
                'class="home-service-icon" aria-hidden="true"'
            ),
            5,
        )

        for service_name in service_names:
            self.assertIn(f'<h3>{service_name}</h3>', services)

        self.assertIn('id="service-project-fit"', services)
        self.assertIn(
            'href="#start-a-project" '
            'aria-label="Go to the Start a Project form"',
            services,
        )
        self.assertIn(
            'target="_blank" rel="noopener noreferrer" '
            'aria-label="Download the Hroman Codes services deck '
            '(opens in a new tab)"',
            services,
        )
        self.assertNotIn('<script', services)

    def test_home_css_defines_services_b_responsive_and_motion_contract(self):
        home_css_path = finders.find('pages/home.css')

        self.assertIsNotNone(home_css_path)
        css = Path(home_css_path).read_text(encoding='utf-8')

        for contract in (
            '.home-page .home-services {',
            '.home-page .home-service-ledger { border-top:',
            '.home-page .home-service-row-featured {',
            'grid-template-columns: 92px minmax(240px, 0.9fr) '
            'minmax(330px, 1.1fr) 42px;',
            '@media (max-width: 980px)',
            '@media (max-width: 760px)',
            '@media (max-width: 560px)',
            '.home-page .home-service-outcomes { grid-column: 2; }',
            '.home-page .home-service-outcomes { grid-column: 1; }',
            '@media (hover: hover) and (pointer: fine)',
            '.home-page .home-service-period:hover '
            '.home-period-pixels i',
            '@media (prefers-reduced-motion: reduce)',
            '.home-page .home-service-period { animation: none;',
            '.home-page .home-service-fit-link:hover { transform: none; }',
        ):
            self.assertIn(contract, css)

    def test_home_renders_case_studies_b_contract(self):
        case_studies = render_to_string('includes/case_studies.html')
        case_names = (
            'Empowered Path Therapy',
            'Rubix AI',
            'LinkTag',
            'Change Food For Good',
            'cThink',
        )
        artifact_urls = (
            'https://www.empoweredpaththerapy.com',
            'https://www.figma.com/design/fNgk1FRaKhQxTCskFZpnwx/EPT',
            'https://www.linkedin.com/company/rubix-tech-ai/posts/',
            'https://www.figma.com/design/5Qd4LC0HDaccNVGKWOiS1G/Rubix_AI',
            'https://www.figma.com/proto/sWPthTO7GABWLjOiMERhHn/'
            'Rubix_HR_Codes',
            'https://hromancodes.s3.us-east-1.amazonaws.com/static/pages/'
            'Rubix_Software_System_Design.drawio.pdf',
            'https://linktag.fly.dev',
            'https://github.com/hroman-codes/link_tag',
            'https://plantid-heriberto.fly.dev',
            'https://github.com/heriberto-codes/plantID',
            'https://changefoodforgood.org/',
            'https://github.com/hroman-codes/cThink',
        )

        self.assertIn(
            '<section id="proof" class="home-case-studies" '
            'aria-labelledby="home-case-studies-title" '
            'data-home-case-studies>',
            case_studies,
        )
        self.assertIn('<h2 id="home-case-studies-title">', case_studies)
        self.assertNotIn('<h1', case_studies)
        self.assertIn('role="tablist" aria-label="Case study type"', case_studies)
        self.assertIn(
            'role="tab" id="home-case-tab-client" aria-selected="true" '
            'aria-controls="home-case-panel-client" tabindex="0"',
            case_studies,
        )
        self.assertIn(
            'role="tab" id="home-case-tab-product" aria-selected="false" '
            'aria-controls="home-case-panel-product" tabindex="-1"',
            case_studies,
        )
        self.assertIn(
            'id="home-case-panel-client" role="tabpanel" '
            'aria-labelledby="home-case-tab-client" data-home-case-panel>',
            case_studies,
        )
        self.assertIn(
            'id="home-case-panel-product" role="tabpanel" '
            'aria-labelledby="home-case-tab-product" data-home-case-panel>',
            case_studies,
        )

        positions = [case_studies.index(name) for name in case_names]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(case_studies.count('class="home-trail-case"'), 5)
        for step_name in ('Understand', 'Build', 'Show'):
            self.assertEqual(
                case_studies.count(f'<li><span>{step_name}</span>'),
                5,
            )
        self.assertEqual(case_studies.count('<details'), 5)
        self.assertEqual(case_studies.count('<details open>'), 2)
        self.assertEqual(
            case_studies.count(
                'target="_blank" rel="noopener noreferrer"'
            ),
            len(artifact_urls),
        )
        for artifact_url in artifact_urls:
            self.assertIn(artifact_url, case_studies)

        for asset_name in ('linktag-home.jpg', 'plantid-main.png'):
            static_path = f'pages/images/{asset_name}'
            self.assertIn(static(static_path), case_studies)
            self.assertIsNotNone(finders.find(static_path))

        self.assertIn('<noscript>', case_studies)
        self.assertIn('both shown below', case_studies)
        self.assertIn(
            'href="#start-a-project" '
            'aria-label="Go to the Start a Project form"',
            case_studies,
        )
        self.assertNotIn('<script', case_studies)

    def test_home_css_defines_case_studies_b_contract(self):
        home_css_path = finders.find('pages/home.css')

        self.assertIsNotNone(home_css_path)
        css = Path(home_css_path).read_text(encoding='utf-8')

        for contract in (
            '.home-page .home-case-studies {',
            '.home-page .home-case-rail { align-self: start; '
            'position: sticky;',
            '.home-page .home-case-tabs {',
            'display: none;',
            '.home-page .home-case-studies.is-enhanced '
            '.home-case-tabs { display: grid; }',
            '.home-page .home-case-studies:not(.is-enhanced) '
            '.home-work-panel + .home-work-panel',
            '.home-page .home-artifact-list-four { '
            'grid-template-columns: repeat(2, minmax(0, 1fr)); }',
            '@media (max-width: 1080px)',
            '@media (max-width: 760px)',
            '@media (max-width: 460px)',
            '.home-page .home-trail-steps { grid-template-columns: 1fr; }',
            '@media (prefers-reduced-motion: reduce)',
            '.home-page .home-case-period { animation: none;',
        ):
            self.assertIn(contract, css)

    def test_home_javascript_defines_case_study_tab_contract(self):
        home_js_path = finders.find('pages/home.js')

        self.assertIsNotNone(home_js_path)
        javascript = Path(home_js_path).read_text(encoding='utf-8')

        for behavior in (
            'const section = document.querySelector('
            '"[data-home-case-studies]");',
            'if (!section) return;',
            'item.setAttribute("aria-selected", String(selected));',
            'item.tabIndex = selected ? 0 : -1;',
            'panel.hidden = panel.id !== tab.getAttribute("aria-controls");',
            'index.hidden = index.dataset.homeCaseIndex !== tab.id;',
            'tab.addEventListener("click", () => selectTab('
            'tab, { preserveViewport: true }));',
            '["ArrowLeft", "ArrowRight", "Home", "End"]',
            'window.location.hash === "#case-cthink"',
            'section.classList.add("is-enhanced");',
            'window.addEventListener("hashchange", selectTabForHash);',
        ):
            self.assertIn(behavior, javascript)

    def test_home_renders_development_process_d_contract(self):
        development_process = render_to_string(
            'includes/development_process.html'
        )
        stage_names = ('Idea', 'Prototype', 'MVP', 'Product', 'Iterate')
        artifact_classes = (
            'home-process-discovery',
            'home-process-wireframes',
            'home-process-release',
            'home-process-product-visual',
            'home-process-feedback',
        )

        self.assertIn(
            '<section id="process" class="home-process" '
            'aria-labelledby="home-process-title">',
            development_process,
        )
        self.assertIn('<h2 id="home-process-title">', development_process)
        self.assertNotIn('<h1', development_process)
        self.assertIn(
            '<ol class="home-process-canvas">',
            development_process,
        )
        self.assertEqual(
            development_process.count('<li class="home-process-piece '),
            5,
        )

        stage_positions = [
            development_process.index(f'<h3>{stage_name}</h3>')
            for stage_name in stage_names
        ]
        self.assertEqual(stage_positions, sorted(stage_positions))

        for artifact_class in artifact_classes:
            self.assertIn(
                f'class="home-process-artifact {artifact_class}" '
                'aria-hidden="true"',
                development_process,
            )

        self.assertIn(
            '<div class="home-process-conversation">',
            development_process,
        )
        self.assertIn(
            'href="#start-a-project" '
            'aria-label="Go to the Start a Project form"',
            development_process,
        )
        self.assertNotIn('<footer', development_process)
        self.assertNotIn('<script', development_process)

    def test_home_css_defines_development_process_d_contract(self):
        home_css_path = finders.find('pages/home.css')

        self.assertIsNotNone(home_css_path)
        css = Path(home_css_path).read_text(encoding='utf-8')

        for contract in (
            '--supporting-copy-size: '
            'clamp(0.94rem, 1.3vw, 1.06rem);',
            '.home-page .home-process {',
            '.home-page .home-process-note p:first-child { '
            'color: var(--grey); '
            'font-size: var(--supporting-copy-size); '
            'line-height: 1.7;',
            '.home-page .home-process-note p:last-child { '
            'color: var(--grey); '
            'font-size: var(--supporting-copy-size);',
            'grid-template-columns: repeat(12, minmax(0, 1fr));',
            '@media (max-width: 1150px)',
            '@media (max-width: 760px)',
            '.home-page .home-process-canvas { '
            'grid-template-columns: 1fr; }',
            '@media (hover: hover) and (pointer: fine) and '
            '(prefers-reduced-motion: no-preference)',
            '.home-page .home-process-piece:hover { '
            'animation: home-process-card-shake 320ms ease-out; }',
            '@media (prefers-reduced-motion: reduce)',
            '.home-page .home-process-period { animation: none;',
            '.home-page .home-process-piece:hover { '
            'animation: none; transform: none; }',
        ):
            self.assertIn(contract, css)

    def test_home_renders_about_a_semantic_and_destination_contract(self):
        about = render_to_string('includes/about.html')
        portrait_path = finders.find('pages/images/aboutMeImage.png')
        skills = (
            ('coding', 'Coding', '25'),
            ('communication', 'Communication', '35'),
            ('design', 'Design', '10'),
            ('process', 'Process', '20'),
            ('tools', 'Technical tools', '10'),
        )

        self.assertIn(
            '<section class="home-about" id="about" '
            'aria-labelledby="home-about-title">',
            about,
        )
        self.assertIn('<h2 id="home-about-title">', about)
        self.assertNotIn('<h1', about)
        self.assertIn(
            f'src="{static("pages/images/aboutMeImage.png")}" '
            'alt="Heriberto Roman, founder of Hroman Codes"',
            about,
        )
        self.assertIsNotNone(portrait_path)
        self.assertIn('Founder + Principal Software Engineer', about)
        self.assertIn(
            'turn ideas and business problems into production-ready '
            'software',
            about,
        )

        self.assertEqual(about.count('class="home-skill-slice '), 5)
        self.assertEqual(about.count('<li class="home-skill-'), 5)
        for slug, label, percentage in skills:
            self.assertIn(
                f'class="home-skill-slice home-skill-{slug}" '
                f'href="#home-skill-{slug}" '
                f'aria-label="{label}, {percentage} percent"',
                about,
            )
            self.assertIn(
                f'class="home-skill-{slug}" id="home-skill-{slug}"',
                about,
            )
            self.assertIn(f'<b>{label}</b><span>{percentage}%</span>', about)

        self.assertIn(
            '<svg class="home-skillset-donut" viewBox="0 0 180 180" '
            'role="group" aria-labelledby="home-skill-chart-title '
            'home-skill-chart-description">',
            about,
        )
        self.assertIn(
            '<title id="home-skill-chart-title">'
            'Interactive skillset balance</title>',
            about,
        )
        self.assertIn(
            '<figcaption class="home-visually-hidden">'
            'Self-described skillset balance: Coding 25%, Communication '
            '35%, Design 10%, Process 20%, and Technical Tools 10%.'
            '</figcaption>',
            about,
        )
        self.assertIn(
            'src="https://www.youtube.com/embed/'
            'jU_VX6YShFI?si=eNtdLXrAJ9XMqSOm" '
            'title="CodeWars Kata 6 — Find Maximum and Minimum" '
            'loading="lazy" '
            'referrerpolicy="strict-origin-when-cross-origin"',
            about,
        )
        self.assertIn('allowfullscreen></iframe>', about)

        for destination in (
            'https://www.youtube.com/@heriberto_codes',
            'https://hromancodes.s3.us-east-1.amazonaws.com/static/pages/'
            'HRomandevresume_April_2026.pdf',
            'https://calendly.com/heriberto_codes/coffee_chat',
        ):
            self.assertIn(
                f'href="{destination}" target="_blank" '
                'rel="noopener noreferrer"',
                about,
            )

        self.assertIn('>View résumé ', about)
        self.assertNotIn(' download', about)
        self.assertNotIn('<script', about)

    def test_home_css_defines_about_a_interaction_and_fallback_contract(self):
        home_css_path = finders.find('pages/home.css')

        self.assertIsNotNone(home_css_path)
        css = Path(home_css_path).read_text(encoding='utf-8')

        for contract in (
            '.home-page .home-about {',
            '.home-page .home-about-portrait-column { align-self: start; '
            'position: sticky;',
            '.home-page .home-skill-slice:is(:hover, :focus) '
            '.home-skill-slice-shape',
            '.home-page .home-skill-slice:focus-visible circle { '
            'stroke-width: 47; }',
            '@media (hover: hover) and (pointer: fine)',
            '@media (max-width: 1000px)',
            '.home-page .home-profile-actions { flex-direction: column; }',
            '.home-page .home-about-action { width: 100%; }',
            '@media (max-width: 760px)',
            '.home-page .home-about-story { display: contents; }',
            '.home-page .home-about-portrait-column { order: 3; '
            'position: static;',
            '.home-page .home-skillset { order: 5; }',
            '.home-page .home-watch-build { order: 6; }',
            '.home-page .home-profile-footer { order: 7;',
            '@media (max-width: 430px)',
            '@media (prefers-reduced-motion: reduce)',
            '.home-page .home-about-period { animation: none;',
            '{ filter: none; transform: none; }',
        ):
            self.assertIn(contract, css)

        for skill in (
            'coding',
            'communication',
            'design',
            'process',
            'tools',
        ):
            self.assertIn(
                '.home-page .home-skillset:has('
                f'.home-skill-slice.home-skill-{skill}:'
                'is(:hover, :focus)) .home-skillset-legend '
                f'.home-skill-{skill}',
                css,
            )
            self.assertIn(
                '.home-page .home-skillset:has('
                f'.home-skillset-legend .home-skill-{skill}:hover) '
                f'.home-skill-slice.home-skill-{skill} '
                '.home-skill-slice-shape',
                css,
            )

    def test_home_css_defines_project_builder_progressive_contract(self):
        home_css_path = finders.find('pages/home.css')

        self.assertIsNotNone(home_css_path)
        css = Path(home_css_path).read_text(encoding='utf-8')

        for contract in (
            '.home-page .home-start-project {',
            '.home-page .home-step-progress { display: none; }',
            '.home-page .home-brief-builder.is-enhanced '
            '.home-step-progress {',
            '.home-page .home-brief-builder.is-enhanced '
            '.home-builder-step:not(.is-active) { display: none; }',
            '.home-page .home-next-button,\n'
            '.home-page .home-back-button { display: none; }',
            '.home-page .home-brief-builder.is-enhanced '
            '.home-next-button,',
            '.home-page .home-submit-button { display: flex; }',
            '.home-page .home-step-actions button { animation: none;',
            '.home-page .home-back-button:hover { background: var(--peach); '
            'border-color: var(--peach); box-shadow: none; '
            'color: var(--navy-deep); transform: translateY(-2px); }',
            '.home-page .home-brief-builder.is-complete '
            '.home-builder-form { display: none; }',
            '@media (max-width: 1020px)',
            '@media (max-width: 700px)',
            '.home-page .home-work-options,',
            '@media (prefers-reduced-motion: reduce)',
            '.home-page .home-project-period { animation: none;',
        ):
            self.assertIn(contract, css)

    def test_home_javascript_defines_project_builder_contract(self):
        home_js_path = finders.find('pages/home.js')

        self.assertIsNotNone(home_js_path)
        javascript = Path(home_js_path).read_text(encoding='utf-8')

        for behavior in (
            'const section = document.querySelector('
            '"[data-home-project]");',
            'const parsedInitialStep = Number(form.dataset.initialStep);',
            'const validatePanel = (panel, { focus = true } = {}) => {',
            'const showStep = (stepNumber, { focusHeading = false, '
            'scroll = false } = {}) => {',
            'step.hidden = !active;',
            'button.disabled = target > furthestStep;',
            'updateChoiceSummary("work_area", summary.area);',
            'updateChoiceSummary("project_stage", summary.stage);',
            'form.noValidate = true;',
            'firstInvalidStep = Number(step.dataset.homeStep);',
            'event.preventDefault();',
            'firstInvalidControl?.focus({ preventScroll: true });',
            'builder.classList.add("is-complete");',
            'success.hidden = true;',
        ):
            self.assertIn(behavior, javascript)

    def test_home_renders_approved_landmark_order(self):
        response = self.client.get(self.base_url)
        parser = HomepageLandmarkParser()
        parser.feed(response.content.decode())

        self.assertEqual(
            parser.landmarks,
            [
                'hero',
                'services',
                'proof',
                'process',
                'insights',
                'about',
                'start-a-project',
                'footer',
            ],
        )

    def test_home_renders_footer_b_contract(self):
        footer = render_to_string('includes/footer.html')
        route_board = (
            ('01', '#services', 'Services'),
            ('02', '#proof', 'Case Studies'),
            ('03', '#process', 'Development Process'),
            ('04', '#insights', 'Insights'),
            ('05', '#about', 'About Heriberto'),
            ('06', '#start-a-project', 'Start a Project'),
        )

        self.assertIn(
            '<footer class="home-site-footer" id="site-footer" '
            'aria-labelledby="home-footer-title">',
            footer,
        )
        self.assertIn('<h2 id="home-footer-title">', footer)
        self.assertNotIn('<h1', footer)
        self.assertIn('07 / The closing signal', footer)
        self.assertEqual(footer.count('<i></i>'), 8)
        self.assertIn(
            'class="home-footer-primary" href="#start-a-project"',
            footer,
        )
        self.assertIn(
            'href="https://calendly.com/heriberto_codes/coffee_chat" '
            'target="_blank" rel="noopener noreferrer"',
            footer,
        )
        self.assertIn('href="mailto:build@heriberto.codes"', footer)
        self.assertIn(
            f'src="{static("pages/images/hr.svg")}" alt=""',
            footer,
        )

        route_positions = []
        for number, target, label in route_board:
            route_markup = (
                f'<a href="{target}"><span>{number}</span>'
                f'<b>{label}</b>'
            )
            self.assertIn(
                route_markup,
                footer,
            )
            route_positions.append(footer.index(route_markup))

        self.assertEqual(route_positions, sorted(route_positions))

        for url, label in (
            ('https://www.linkedin.com/in/heribertoroman/', 'LinkedIn'),
            ('https://github.com/heriberto-codes', 'GitHub'),
            ('https://www.youtube.com/@heriberto_codes', 'YouTube'),
        ):
            self.assertIn(
                f'<a href="{url}" target="_blank" '
                f'rel="noopener noreferrer">{label}',
                footer,
            )

        self.assertEqual(
            footer.count(
                'target="_blank" rel="noopener noreferrer"'
            ),
            4,
        )

        self.assertIn('© 2026 Hroman Codes, LLC.', footer)
        self.assertIn('Designed &amp; engineered by Heriberto Roman.', footer)
        self.assertIn(
            'href="#top">Return to the beginning',
            footer,
        )

    def test_home_preserves_heading_number_and_fragment_continuity(self):
        response = self.client.get(self.base_url)
        content = response.content.decode()
        parser = HomepageContinuityParser()
        parser.feed(content)

        self.assertEqual(parser.heading_one_count, 1)
        numbered_sections = (
            '01 / Services',
            '02 / Case Studies',
            '03 / Development Process',
            '04 / Insights',
            '05 / About Heriberto Roman',
            '06 / Start a Project',
            '07 / The closing signal',
        )
        positions = [content.index(label) for label in numbered_sections]
        self.assertEqual(positions, sorted(positions))

        for target in set(parser.fragment_targets):
            self.assertIn(target, parser.ids)
            self.assertEqual(parser.ids.count(target), 1)

    def test_home_css_defines_footer_b_responsive_and_motion_contract(self):
        home_css_path = finders.find('pages/home.css')

        self.assertIsNotNone(home_css_path)
        css = Path(home_css_path).read_text(encoding='utf-8')

        for contract in (
            '.home-page .home-site-footer {',
            '.home-page .home-footer-hero {',
            '.home-page .home-footer-route-board {',
            '.home-page .home-footer-status p { color: var(--navy-deep);',
            '.home-page .home-footer-actions a { align-items: center; '
            'border: 1px solid var(--navy-deep); '
            'color: var(--navy-deep) !important;',
            '.home-page .home-footer-actions .home-footer-primary { '
            'background: var(--navy-deep); '
            'color: var(--cream) !important; }',
            '.home-page .home-footer-actions a:hover { '
            'background: var(--cream); '
            'color: var(--navy-deep) !important; }',
            '.home-page .home-footer-routes a { align-items: center; '
            'border-bottom: 1px solid var(--line-dark); '
            'color: var(--navy-deep) !important;',
            '.home-page .home-footer-routes a:hover { '
            'color: var(--peach-deep) !important; }',
            '.home-page .home-footer-social a { '
            'border-bottom: 1px solid var(--line-dark); '
            'color: var(--navy-deep) !important;',
            '.home-page .home-footer-social a:hover { '
            'color: var(--peach-deep) !important; }',
            'grid-template-columns: minmax(320px, 0.9fr) '
            'minmax(440px, 1.25fr) minmax(220px, 0.55fr);',
            '@media (max-width: 1060px)',
            '@media (max-width: 700px)',
            '@media (max-width: 410px)',
            '.home-page .home-footer-route-board { '
            'grid-template-columns: 1fr; }',
            '.home-page .home-footer-base { grid-template-columns: 1fr; }',
            '@media (prefers-reduced-motion: reduce)',
            '.home-page .home-footer-status > span { animation: none; }',
            '.home-page .home-footer-period .home-period-pixels { '
            'display: none; }',
            '.home-page .home-footer-routes a:hover i { transform: none; }',
        ):
            self.assertIn(contract, css)

    def test_home_uses_new_section_partials_without_legacy_sections(self):
        response = self.client.get(self.base_url)

        for template_name in (
            'includes/services.html',
            'includes/case_studies.html',
            'includes/development_process.html',
            'includes/insights.html',
            'includes/start_project.html',
        ):
            self.assertTemplateUsed(response, template_name)

        for template_name in (
            'includes/experience.html',
            'includes/tools.html',
            'includes/work.html',
            'includes/blog_home_page.html',
            'includes/contact.html',
        ):
            self.assertTemplateNotUsed(response, template_name)

    def test_base_template_keeps_default_non_home_scope(self):
        rendered_base = render_to_string('base.html')

        self.assertIn(
            '<meta name="description" content="Hroman Codes builds reliable '
            'digital products, practical automation, and scalable software.">',
            rendered_base,
        )
        self.assertIn('<body class="hrBody">', rendered_base)
        self.assertNotIn('home-page', rendered_base)
        self.assertNotIn(static('pages/home.css'), rendered_base)

        child_template = engines['django'].from_string(
            """
            {% extends 'base.html' %}
            {% block page_meta %}<meta name="robots" content="noindex">{% endblock %}
            {% block page_styles %}<link rel="stylesheet" href="/test-page.css">{% endblock %}
            {% block body_class %}hrBody test-page{% endblock %}
            {% block content %}<main>Test page</main>{% endblock %}
            {% block page_scripts %}<script src="/test-page.js"></script>{% endblock %}
            """
        )
        rendered_child = child_template.render({})

        for marker in (
            '<meta name="robots" content="noindex">',
            '<link rel="stylesheet" href="/test-page.css">',
            '<body class="hrBody test-page">',
            '<script src="/test-page.js"></script>',
        ):
            self.assertIn(marker, rendered_child)

    def test_home_css_defines_scoped_responsive_foundation(self):
        home_css_path = finders.find('pages/home.css')

        self.assertIsNotNone(home_css_path)
        css = Path(home_css_path).read_text(encoding='utf-8')

        for token in (
            '--navy:',
            '--cream:',
            '--page-max-width:',
            '--page-gutter:',
            '--section-space:',
        ):
            self.assertIn(token, css)

        self.assertIn('.home-page', css)
        self.assertIn(':focus-visible', css)
        self.assertIn('@media (max-width: 700px)', css)
        self.assertIn('@media (max-width: 860px)', css)
        self.assertIn('@media (max-width: 480px)', css)
        self.assertIn('grid-template-columns: repeat(3, 1fr)', css)
        self.assertIn(
            'background-image: url("images/heriberto-working.jpg")',
            css,
        )
        self.assertIn(
            '.home-page .home-pixel-word-text { display: inline-block; '
            'filter: blur(0)',
            css,
        )
        self.assertIn(
            '.home-page .home-pixel-word.is-pixelated '
            '.home-pixel-word-text { filter: blur(2px); opacity: 0; }',
            css,
        )
        self.assertIn(
            '.home-page .home-pixel-word.is-pixelated '
            '.home-pixel-word-canvas { filter: blur(0); opacity: 1;',
            css,
        )
        self.assertIn('@media (prefers-reduced-motion: reduce)', css)
        self.assertIn(
            '.home-page .home-pixel-word-canvas { display: none; }',
            css,
        )
        self.assertIn(
            '.home-page .home-pixel-word-text { filter: none !important; '
            'opacity: 1 !important; }',
            css,
        )
        self.assertIn(
            '.home-page .home-mosaic-grid span { transform: none; }',
            css,
        )

    def test_home_javascript_defines_navigation_and_headline_safeguards(self):
        home_js_path = finders.find('pages/home.js')

        self.assertIsNotNone(home_js_path)
        javascript = Path(home_js_path).read_text(encoding='utf-8')

        for behavior in (
            'links.forEach((link) => link.addEventListener("click", '
            '() => closeMenu()));',
            'document.addEventListener("pointerdown", (event) => {',
            'if (menu.open && !menu.contains(event.target)) closeMenu();',
            'if (event.key === "Escape" && menu.open) '
            'closeMenu({ returnFocus: true });',
            'if (returnFocus) summary.focus();',
            'reducedMotion.matches ? 0 : 270',
            'if (!word || !canvas || !text || reducedMotion.matches) return;',
            'if (!context) return;',
            'word.classList.remove("is-revealing", "is-pixelated");',
        ):
            self.assertIn(behavior, javascript)
