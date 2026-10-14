from django.template.loader import render_to_string
from django.test import Client, TestCase
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import escape

from apps.blog.models import Like, Post
from apps.blog.tests.test_like_views import LikeFormParser
from apps.blog.views import (
    GUARDRAILS_CHAPTERS,
    GUARDRAILS_INSIGHT_SLUG,
    RELATED_INSIGHT_CHANNELS,
    _guardrails_transcript,
)


def guardrails_body(payload_count=3):
    body_parts = ['<p>Guardrails introduction.</p>']
    for chapter in GUARDRAILS_CHAPTERS:
        body_parts.extend(
            (
                f'<h2>{chapter["heading"]}</h2>',
                f'<p>Chapter {chapter["number"]} copy.</p>',
            )
        )

    body_parts.append('<h2>Highlander React/Redux Project</h2>')
    payload_links = (
        ('Demo', 'https://example.com/demo?mode=full&amp;source=cms'),
        ('Source', 'https://example.com/source'),
        ('Workflow', 'https://example.com/workflow'),
    )
    body_parts.extend(
        f'<a href="{href}">{label}</a>'
        for label, href in payload_links[:payload_count]
    )
    return ''.join(body_parts)


class TestBlogViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.base_url = reverse('blog_index')
        self.standard_post = Post.objects.create(
            title='Standard article',
            slug='standard-article',
            snippet='A standard article.',
            body='<p>Standard article body.</p>',
            status=1,
        )
        self.blog_detail_url = self.standard_post.get_absolute_url()
        self.blog_category_url = reverse(
            'blog_category',
            kwargs={'category': 'category'},
        )

    def create_guardrails_post(self, **overrides):
        values = {
            'title': 'Turtle AI guardrails',
            'slug': GUARDRAILS_INSIGHT_SLUG,
            'snippet': 'A Guardrails signal transcript.',
            'body': guardrails_body(),
            'status': 1,
        }
        values.update(overrides)
        return Post.objects.create(**values)

    def test_can_load_base_blog_template(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/base_blog.html')
        
    def test_can_load_blog_index_template(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_index.html')

    def test_blog_index_keeps_non_home_page_scope(self):
        response = self.client.get(self.base_url)

        self.assertContains(response, '<body class="hrBody">')
        self.assertNotContains(response, 'class="hrBody home-page"')
        self.assertNotContains(
            response,
            f'href="{static("pages/home.css")}"',
        )
          
    def test_can_load_blog_detail_template(self):
        response = self.client.get(self.blog_detail_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_detail.html')
        self.assertTemplateNotUsed(response, 'blog/insight_detail.html')

    def test_article_reads_preserve_missing_zero_and_positive_likes(self):
        for count in (None, 0, 5):
            for feedback in (False, True):
                with self.subTest(count=count, feedback=feedback):
                    Like.objects.all().delete()
                    like = None if count is None else Like.objects.create(
                        post=self.standard_post, like=count,
                    )
                    client = Client(enforce_csrf_checks=True)
                    session = client.session
                    session['liked_posts'] = [self.standard_post.pk]
                    session['unrelated_value'] = 'preserve-me'
                    session.save()
                    session_before = dict(client.session)
                    rows_before = list(Like.objects.values_list(
                        'pk', 'post_id', 'like',
                    ))
                    url = self.blog_detail_url
                    if feedback:
                        url += '?liked=true'

                    for method in ('get', 'get', 'head'):
                        response = getattr(client, method)(url)

                        self.assertEqual(response.status_code, 200)
                        self.assertTemplateUsed(
                            response, 'blog/blog_detail.html',
                        )
                        self.assertEqual(response.context['like'], like)
                        self.assertEqual(
                            response.context['post_was_liked'], feedback,
                        )
                        if method == 'get':
                            self.assertContains(
                                response, f'<small>{count or 0}</small>',
                                html=True,
                            )
                            icon = LikeFormParser(
                                response.content.decode(),
                            ).forms[0]['icons'][0]
                            self.assertIn(
                                'fa-solid' if feedback else 'fa-regular',
                                icon['class'].split(),
                            )
                        else:
                            self.assertEqual(response.content, b'')
                        self.assertEqual(
                            list(Like.objects.values_list(
                                'pk', 'post_id', 'like',
                            )),
                            rows_before,
                        )
                        self.assertEqual(dict(client.session), session_before)

    def assert_like_forms(self, content, posts):
        parsed = LikeFormParser(content)
        expected_actions = [
            reverse('like_post', args=[post.pk, post.slug]) for post in posts
        ]
        self.assertCountEqual(
            [form['action'] for form in parsed.forms], expected_actions,
        )
        self.assertFalse(any(
            anchor.get('href', '').startswith('/blog/liked/')
            for anchor in parsed.anchors
        ))
        by_action = {form['action']: form for form in parsed.forms}
        for post, action in zip(posts, expected_actions):
            form = by_action[action]
            self.assertEqual(form['method'], 'post')
            tokens = [
                field for field in form['inputs']
                if field.get('name') == 'csrfmiddlewaretoken'
            ]
            self.assertEqual(len(tokens), 1)
            self.assertEqual(tokens[0]['type'], 'hidden')
            self.assertTrue(tokens[0].get('value'))
            self.assertEqual(len(form['buttons']), 1)
            button = form['buttons'][0]
            self.assertEqual(button['type'], 'submit')
            self.assertIn('blog-like-button', button['class'].split())
            self.assertEqual(button['aria-label'], f'Like {post.title}')
            self.assertIn(f'aria-label="Like {escape(post.title)}"', content)
            self.assertEqual(len(form['icons']), 1)
            self.assertEqual(form['icons'][0]['aria-hidden'], 'true')
        return parsed.forms

    def test_all_like_callers_render_working_internal_post_forms(self):
        self.standard_post.title = 'Article "quoted" <b>& text'
        self.standard_post.save(update_fields=['title'])
        draft = Post.objects.create(
            title='Draft without a Like control', slug='draft-without-like',
            snippet='Draft.', status=0,
        )
        draft_action = reverse('like_post', args=[draft.pk, draft.slug])

        for surface in ('detail', 'index', 'legacy_include'):
            with self.subTest(surface=surface):
                Like.objects.all().delete()
                client = Client(enforce_csrf_checks=True)
                url = (
                    self.blog_detail_url if surface == 'detail'
                    else self.base_url
                )
                response = client.get(url)
                self.assertEqual(response.status_code, 200)
                content = response.content.decode()
                if surface == 'legacy_include':
                    content = render_to_string(
                        'includes/blog_home_page.html',
                        {'posts': [self.standard_post, draft]},
                        request=response.wsgi_request,
                    )
                forms = self.assert_like_forms(content, [self.standard_post])
                self.assertNotIn(draft_action, content)
                self.assertFalse(Like.objects.exists())
                self.assertNotIn('liked_posts', client.session)
                token = next(
                    field['value'] for field in forms[0]['inputs']
                    if field.get('name') == 'csrfmiddlewaretoken'
                )

                submitted = client.post(
                    forms[0]['action'], {'csrfmiddlewaretoken': token},
                    HTTP_ORIGIN='http://testserver',
                )

                self.assertRedirects(
                    submitted, f'{self.blog_detail_url}?liked=true',
                    fetch_redirect_response=False,
                )
                self.assertEqual(
                    Like.objects.get(post=self.standard_post).like, 1,
                )
                self.assertEqual(
                    client.session['liked_posts'], [self.standard_post.pk],
                )

    def test_blog_detail_rejects_mismatched_slug(self):
        mismatched_url = reverse(
            'blog_detail',
            kwargs={'pk': self.standard_post.pk, 'slug': 'wrong-slug'},
        )

        response = self.client.get(mismatched_url)

        self.assertEqual(response.status_code, 404)

    def test_blog_detail_rejects_draft_post(self):
        draft_post = Post.objects.create(
            title='Draft article',
            slug='draft-article',
            snippet='A draft article.',
            body='<p>Draft content.</p>',
            status=0,
        )

        response = self.client.get(draft_post.get_absolute_url())

        self.assertEqual(response.status_code, 404)

    def test_guardrails_post_uses_signal_transcript_contract(self):
        guardrails_post = self.create_guardrails_post()

        response = self.client.get(guardrails_post.get_absolute_url())

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/insight_detail.html')
        self.assertTemplateNotUsed(response, 'blog/blog_detail.html')
        self.assertEqual(LikeFormParser(response.content.decode()).forms, [])
        self.assertContains(
            response,
            f'href="{static("blog/insight_detail.css")}"',
        )
        self.assertEqual(response.content.count(b'<h1'), 1)
        for chapter in GUARDRAILS_CHAPTERS:
            self.assertContains(response, f'id="{chapter["id"]}"')
        self.assertContains(
            response,
            'target="_blank" rel="noopener noreferrer"',
            count=3,
        )

    def test_guardrails_related_signals_are_published_and_ordered(self):
        guardrails_post = self.create_guardrails_post()
        first_channel, second_channel = RELATED_INSIGHT_CHANNELS
        second_post = Post.objects.create(
            title='Second configured signal',
            slug=second_channel['slug'],
            snippet='Second signal.',
            status=1,
        )
        first_post = Post.objects.create(
            title='First configured signal',
            slug=first_channel['slug'],
            snippet='First signal.',
            status=1,
        )
        Post.objects.create(
            title='Unconfigured signal',
            slug='unconfigured-signal',
            snippet='Not part of the configured channels.',
            status=1,
        )

        response = self.client.get(guardrails_post.get_absolute_url())

        self.assertEqual(
            [
                signal['post'].slug
                for signal in response.context['related_signals']
            ],
            [channel['slug'] for channel in RELATED_INSIGHT_CHANNELS],
        )

        second_post.status = 0
        second_post.save(update_fields=['status'])
        response = self.client.get(guardrails_post.get_absolute_url())

        self.assertEqual(
            [signal['post'] for signal in response.context['related_signals']],
            [first_post],
        )

    def test_guardrails_uses_archive_fallback_without_related_posts(self):
        guardrails_post = self.create_guardrails_post()

        response = self.client.get(guardrails_post.get_absolute_url())

        self.assertEqual(response.context['related_signals'], [])
        self.assertContains(response, reverse('blog_index'))
        self.assertContains(response, 'Browse the Insights archive')

    def test_can_load_blog_category(self):
        response = self.client.get(self.blog_category_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_category.html')


class TestGuardrailsTranscript(TestCase):
    def test_transcript_maps_chapters_and_extracts_cms_payloads(self):
        intro, chapters, payloads = _guardrails_transcript(
            guardrails_body()
        )

        self.assertEqual(intro, '<p>Guardrails introduction.</p>')
        self.assertEqual(
            [chapter['id'] for chapter in chapters],
            [chapter['id'] for chapter in GUARDRAILS_CHAPTERS],
        )
        for chapter in chapters:
            self.assertIn(
                f'Chapter {chapter["number"]} copy.',
                chapter['html'],
            )
        self.assertEqual(
            [payload['href'] for payload in payloads],
            [
                'https://example.com/demo?mode=full&source=cms',
                'https://example.com/source',
                'https://example.com/workflow',
            ],
        )
        self.assertNotIn(
            'Highlander React/Redux Project',
            ''.join(chapter['html'] for chapter in chapters),
        )

    def test_transcript_preserves_raw_appendix_when_payload_count_changes(self):
        intro, chapters, payloads = _guardrails_transcript(
            guardrails_body(payload_count=2)
        )

        self.assertEqual(intro, '<p>Guardrails introduction.</p>')
        self.assertEqual(payloads, [])
        self.assertIn(
            '<h2>Highlander React/Redux Project</h2>',
            chapters[-1]['html'],
        )
        self.assertIn(
            'https://example.com/demo?mode=full&amp;source=cms',
            chapters[-1]['html'],
        )
