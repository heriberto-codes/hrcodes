import logging

from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.generic.edit import FormView

from apps.blog.models import Post
from apps.pages.forms import ProjectBriefForm
from apps.pages.throttling import consume_project_inquiry_throttle


logger = logging.getLogger(__name__)

PROJECT_INQUIRY_COOLDOWN_SESSION_KEY = 'project_inquiry_sent_at'
PROJECT_INQUIRY_DELIVERY_ERROR = (
    'Your project brief could not be sent right now. '
    'Please try again shortly or use the scheduling link.'
)


FEATURED_INSIGHT_CHANNELS = (
    {
        'slug': (
            'i-revived-my-reactredux-app-with-turtle-ai-and-learned-where-'
            'ai-guardrails-can-go-too-far'
        ),
        'name': 'Guardrails',
        'number': '01',
        'frequency': '88.7',
        'visual': 'guardrails',
    },
    {
        'slug': 'how-constraints-changed-the-way-i-think-about-algorithms',
        'name': 'Constraints',
        'number': '02',
        'frequency': '91.1',
        'visual': 'constraints',
    },
    {
        'slug': (
            'i-revived-a-9-year-old-app-with-openai-codex-with-a-product-'
            'engineer-mindset'
        ),
        'name': 'Revival',
        'number': '03',
        'frequency': '93.9',
        'visual': 'revival',
    },
)


class HomePageView(FormView):
    template_name = 'home.html'
    form_class = ProjectBriefForm

    def get_success_url(self):
        return f'{reverse("home")}#start-a-project'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slugs = [channel['slug'] for channel in FEATURED_INSIGHT_CHANNELS]
        published_posts = {
            post.slug: post
            for post in Post.objects.filter(
                slug__in=slugs,
                status=1,
            ).prefetch_related('categories')
        }
        insight_signals = [
            {**channel, 'post': published_posts[channel['slug']]}
            for channel in FEATURED_INSIGHT_CHANNELS
            if channel['slug'] in published_posts
        ]
        missing_insight_channels = [
            channel['name']
            for channel in FEATURED_INSIGHT_CHANNELS
            if channel['slug'] not in published_posts
        ]

        context.update({
            'posts': [signal['post'] for signal in insight_signals],
            'insight_signals': insight_signals,
            'insight_signal_count': len(insight_signals),
            'insights_complete': not missing_insight_channels,
            'missing_insight_channels': missing_insight_channels,
        })
        return context

    def form_valid(self, form):
        try:
            allowed = consume_project_inquiry_throttle(self.request)
        except Exception:
            logger.exception('Project inquiry throttle evaluation failed.')
            form.add_error(None, PROJECT_INQUIRY_DELIVERY_ERROR)
            return self.form_invalid(form)

        if not allowed:
            form.add_error(
                None,
                'Please wait a moment before sending another project brief.',
            )
            return self.form_invalid(form)

        cleaned_data = form.cleaned_data
        message = render_to_string(
            'email/project_inquiry.txt',
            {
                'name': cleaned_data['name'],
                'email': cleaned_data['email'],
                'company': cleaned_data['company'],
                'work_area': dict(form.fields['work_area'].choices)[
                    cleaned_data['work_area']
                ],
                'project_stage': dict(form.fields['project_stage'].choices)[
                    cleaned_data['project_stage']
                ],
                'timing': dict(form.fields['timing'].choices)[
                    cleaned_data['timing']
                ],
                'goal': cleaned_data['goal'],
                'additional_context': cleaned_data['additional_context'],
            },
        )
        email = EmailMessage(
            subject='New Hroman Codes project brief',
            body=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[settings.PROJECT_INQUIRY_RECIPIENT],
            reply_to=[cleaned_data['email']],
        )

        try:
            delivered = email.send(fail_silently=False)
        except Exception:
            logger.exception('Project inquiry email delivery failed.')
            form.add_error(None, PROJECT_INQUIRY_DELIVERY_ERROR)
            return self.form_invalid(form)

        if delivered != 1:
            form.add_error(None, PROJECT_INQUIRY_DELIVERY_ERROR)
            return self.form_invalid(form)

        self.request.session[PROJECT_INQUIRY_COOLDOWN_SESSION_KEY] = (
            timezone.now().timestamp()
        )
        messages.success(
            self.request,
            'Your project brief was sent. Thank you for the context.',
        )
        return super().form_valid(form)
