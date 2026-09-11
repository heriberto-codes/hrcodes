from html.parser import HTMLParser
from pathlib import Path

from django.contrib.staticfiles import finders
from django.template import engines
from django.test import TestCase, Client
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse


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

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        if tag == 'section' and attributes.get('id') in self.section_ids:
            self.landmarks.append(attributes['id'])
        elif tag == 'footer':
            self.landmarks.append('footer')


class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url = reverse('home')
            
    def test_can_load_base_template(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')
    
    def test_can_view_home_template(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')

    def test_home_uses_page_scoped_foundation(self):
        response = self.client.get(self.base_url)
        home_css_path = finders.find('pages/home.css')

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
            f'href="{static("pages/home.css")}"',
        )
        self.assertIsNotNone(home_css_path)

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
        self.assertIn('@media (prefers-reduced-motion: reduce)', css)
