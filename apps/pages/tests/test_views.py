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
            f'href="{static("pages/home.css")}"',
        )
        self.assertContains(
            response,
            f'<script src="{static("pages/home.js")}" defer></script>',
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
