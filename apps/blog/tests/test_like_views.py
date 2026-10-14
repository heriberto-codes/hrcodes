from html.parser import HTMLParser

from django.conf import settings
from django.test import Client, TestCase
from django.urls import reverse

from apps.blog.models import Like, Post


class LikeFormParser(HTMLParser):
    """Inspect rendered controls without a third-party HTML library."""

    def __init__(self, content):
        super().__init__()
        self.forms = []
        self.anchors = []
        self.current_form = None
        self.feed(content)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            self.anchors.append(attrs)
        if tag == 'form':
            if 'blog-like-form' in attrs.get('class', '').split():
                self.current_form = {
                    **attrs, 'inputs': [], 'buttons': [], 'icons': [],
                }
                self.forms.append(self.current_form)
        elif self.current_form is not None:
            field = {
                'input': 'inputs', 'button': 'buttons', 'i': 'icons',
            }.get(tag)
            if field:
                self.current_form[field].append(attrs)

    def handle_endtag(self, tag):
        if tag == 'form':
            self.current_form = None


class TestLikeViews(TestCase):
    def setUp(self):
        self.post = Post.objects.create(
            title='Published article',
            slug='published-article',
            snippet='A published article.',
            status=1,
        )
        self.other_post = Post.objects.create(
            title='Another published article',
            slug='another-published-article',
            snippet='Another article.',
            status=1,
        )
        self.draft = Post.objects.create(
            title='Draft article',
            slug='draft-article',
            snippet='A draft article.',
            status=0,
        )
        self.like_url = reverse(
            'like_post',
            kwargs={'pk': self.post.pk, 'slug': self.post.slug},
        )
        self.client = Client(enforce_csrf_checks=True)
        session = self.client.session
        session['liked_posts'] = [self.other_post.pk]
        session['unrelated_value'] = 'preserve-me'
        session.save()

    def rendered_form(self, client):
        response = client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        forms = LikeFormParser(response.content.decode()).forms
        self.assertEqual(len(forms), 1)
        form = forms[0]
        self.assertEqual(form['action'], self.like_url)
        self.assertEqual(form['method'], 'post')
        tokens = [
            field['value'] for field in form['inputs']
            if field.get('name') == 'csrfmiddlewaretoken'
        ]
        self.assertEqual(len(tokens), 1)
        self.assertTrue(tokens[0])
        self.assertIn(settings.CSRF_COOKIE_NAME, client.cookies)
        return form, tokens[0]

    def valid_post(self, client, url, **kwargs):
        _, token = self.rendered_form(client)
        return client.post(
            url, {'csrfmiddlewaretoken': token},
            HTTP_ORIGIN='http://testserver', **kwargs,
        )

    def like_rows(self):
        return list(Like.objects.order_by('pk').values_list(
            'pk', 'post_id', 'like',
        ))

    def assert_state_unchanged(self, client, rows, session):
        self.assertEqual(self.like_rows(), rows)
        self.assertEqual(dict(client.session), session)

    def assert_canonical_redirect(self, response):
        self.assertRedirects(
            response,
            f'{self.post.get_absolute_url()}?liked=true',
            fetch_redirect_response=False,
        )

    def test_published_post_creates_like_and_preserves_session_entries(self):
        response = self.valid_post(self.client, self.like_url)

        self.assert_canonical_redirect(response)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.get(post=self.post).like, 1)
        self.assertEqual(
            dict(self.client.session),
            {
                'liked_posts': [self.other_post.pk, self.post.pk],
                'unrelated_value': 'preserve-me',
            },
        )

    def test_published_post_increments_existing_like_once(self):
        like = Like.objects.create(post=self.post, like=7)

        response = self.valid_post(self.client, self.like_url)

        self.assert_canonical_redirect(response)
        like.refresh_from_db()
        self.assertEqual(like.like, 8)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(
            self.client.session['liked_posts'],
            [self.other_post.pk, self.post.pk],
        )
        self.assertEqual(
            self.client.session['unrelated_value'], 'preserve-me',
        )

    def test_sequential_repeat_preserves_count_and_session(self):
        first_response = self.valid_post(self.client, self.like_url)
        self.assert_canonical_redirect(first_response)
        session_before_repeat = dict(self.client.session)

        repeat_response = self.valid_post(self.client, self.like_url)

        self.assert_canonical_redirect(repeat_response)
        self.assertEqual(Like.objects.count(), 1)
        self.assertEqual(Like.objects.get(post=self.post).like, 1)
        self.assertEqual(dict(self.client.session), session_before_repeat)
        self.assertEqual(
            self.client.session['liked_posts'],
            [self.other_post.pk, self.post.pk],
        )

    def assert_rejected_without_mutation(self, url, post=None):
        session_states = [None, [self.other_post.pk]]
        if post is not None:
            session_states.append([self.other_post.pk, post.pk])

        for existing_like in (False, True):
            for liked_posts in session_states:
                with self.subTest(
                    existing_like=existing_like, liked_posts=liked_posts,
                ):
                    Like.objects.all().delete()
                    if existing_like:
                        Like.objects.create(post=post or self.post, like=7)
                    client = Client(enforce_csrf_checks=True)
                    session = client.session
                    session['unrelated_value'] = 'preserve-me'
                    if liked_posts is not None:
                        session['liked_posts'] = liked_posts
                    session.save()
                    session_before = dict(client.session)
                    likes_before = list(
                        Like.objects.order_by('pk').values_list(
                            'pk', 'post_id', 'like',
                        )
                    )

                    response = self.valid_post(client, url)

                    self.assertEqual(response.status_code, 404)
                    self.assertEqual(
                        list(Like.objects.order_by('pk').values_list(
                            'pk', 'post_id', 'like',
                        )),
                        likes_before,
                    )
                    self.assertEqual(dict(client.session), session_before)

    def test_mismatched_slug_rejected_without_mutation(self):
        url = reverse(
            'like_post',
            kwargs={'pk': self.post.pk, 'slug': self.other_post.slug},
        )

        self.assert_rejected_without_mutation(url, post=self.post)

    def test_draft_rejected_without_mutation(self):
        url = reverse(
            'like_post',
            kwargs={'pk': self.draft.pk, 'slug': self.draft.slug},
        )

        self.assert_rejected_without_mutation(url, post=self.draft)

    def test_missing_post_rejected_without_mutation(self):
        url = reverse(
            'like_post',
            kwargs={'pk': self.draft.pk + 1000, 'slug': self.post.slug},
        )

        self.assert_rejected_without_mutation(url)

    def test_invalid_csrf_posts_never_mutate_likes_or_session(self):
        cases = (
            'missing_cookie', 'missing_token', 'invalid_token', 'bad_origin',
        )
        for existing_like in (False, True):
            for liked_posts in (None, [self.other_post.pk]):
                for case in cases:
                    with self.subTest(
                        existing_like=existing_like, liked_posts=liked_posts,
                        case=case,
                    ):
                        Like.objects.all().delete()
                        if existing_like:
                            Like.objects.create(post=self.post, like=7)
                        client = Client(enforce_csrf_checks=True)
                        session = client.session
                        session['unrelated_value'] = 'preserve-me'
                        if liked_posts is not None:
                            session['liked_posts'] = liked_posts
                        session.save()
                        _, token = self.rendered_form(client)
                        data = {'csrfmiddlewaretoken': token}
                        origin = 'http://testserver'
                        if case == 'missing_cookie':
                            del client.cookies[settings.CSRF_COOKIE_NAME]
                        elif case == 'missing_token':
                            data = {}
                        elif case == 'invalid_token':
                            data['csrfmiddlewaretoken'] = (
                                ('a' if token[0] != 'a' else 'b') + token[1:]
                            )
                        else:
                            origin = 'https://untrusted.example'
                        rows_before = self.like_rows()
                        session_before = dict(client.session)

                        response = client.post(
                            self.like_url, data, HTTP_ORIGIN=origin,
                        )

                        self.assertEqual(response.status_code, 403)
                        self.assert_state_unchanged(
                            client, rows_before, session_before,
                        )

    def test_non_post_methods_never_mutate_likes_or_session(self):
        for existing_like in (False, True):
            for method in ('get', 'head', 'put', 'patch', 'delete'):
                with self.subTest(existing_like=existing_like, method=method):
                    Like.objects.all().delete()
                    if existing_like:
                        Like.objects.create(post=self.post, like=7)
                    _, token = self.rendered_form(self.client)
                    rows_before = self.like_rows()
                    session_before = dict(self.client.session)
                    # Unsafe methods need valid CSRF to reach require_POST.
                    kwargs = {
                        'HTTP_X_CSRFTOKEN': token,
                        'HTTP_ORIGIN': 'http://testserver',
                    } if method not in ('get', 'head') else {}

                    response = getattr(self.client, method)(
                        self.like_url, **kwargs,
                    )

                    self.assertEqual(response.status_code, 405)
                    self.assertEqual(response.headers['Allow'], 'POST')
                    self.assert_state_unchanged(
                        self.client, rows_before, session_before,
                    )

    def test_rendered_form_post_redirect_and_repeat_with_fresh_session(self):
        client = Client(enforce_csrf_checks=True)
        form, token = self.rendered_form(client)
        self.assertNotIn('liked_posts', client.session)
        self.assertEqual(self.like_rows(), [])
        data = {
            'csrfmiddlewaretoken': token,
            'pk': self.other_post.pk,
            'slug': self.other_post.slug,
            'next': 'https://untrusted.example',
        }

        response = client.post(
            form['action'], data, HTTP_ORIGIN='http://testserver', follow=True,
        )

        self.assertEqual(response.redirect_chain, [
            (f'{self.post.get_absolute_url()}?liked=true', 302),
        ])
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<small>1</small>', html=True)
        self.assertTrue(response.context['post_was_liked'])
        button_icon = LikeFormParser(
            response.content.decode(),
        ).forms[0]['icons'][0]
        self.assertIn('fa-solid', button_icon['class'].split())
        self.assertEqual(Like.objects.get(post=self.post).like, 1)
        self.assertFalse(Like.objects.filter(post=self.other_post).exists())
        self.assertEqual(client.session['liked_posts'], [self.post.pk])
        rows_before = self.like_rows()
        session_before = dict(client.session)

        repeated = client.post(
            form['action'], data, HTTP_ORIGIN='http://testserver', follow=True,
        )

        self.assertEqual(repeated.redirect_chain, response.redirect_chain)
        self.assertEqual(repeated.status_code, 200)
        self.assert_state_unchanged(client, rows_before, session_before)
