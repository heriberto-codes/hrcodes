from ckeditor.widgets import CKEditorWidget
from django.conf import settings
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.test import Client, TestCase
from django.urls import reverse

from apps.blog.models import Category, Post


class TestPostAdminAuthoring(TestCase):
    @classmethod
    def setUpTestData(cls):
        original_category = Category.objects.create(name='Original')
        cls.new_category = Category.objects.create(name='Updated')
        cls.draft = Post.objects.create(
            title='Original draft',
            slug='original-draft',
            body='<p>Original body</p>',
            snippet='Original summary',
        )
        cls.draft.categories.add(original_category)

    def setUp(self):
        self.add_url = reverse('admin:blog_post_add')
        self.change_url = reverse('admin:blog_post_change', args=[self.draft.pk])
        self.post_data = {
            'title': 'Rich text article',
            'slug': 'rich-text-article',
            'body': '<p>A <strong>formatted</strong> article.</p>',
            'snippet': '<em>A formatted summary.</em>',
            'status': 1,
            'categories': [self.new_category.pk],
            '_save': 'Save',
        }

    def make_user(self, username, *permissions, is_staff=True, is_active=True):
        user = get_user_model().objects.create_user(
            username, is_staff=is_staff, is_active=is_active,
        )
        user.user_permissions.set(Permission.objects.filter(
            content_type__app_label='blog',
            content_type__model='post',
            codename__in=permissions,
        ))
        return user

    def csrf_client(self, user=None):
        client = Client(enforce_csrf_checks=True)
        if user is not None:
            client.force_login(user)
        # Both the admin index and the login page render a CSRF token.
        response = client.get(reverse('admin:index'), follow=True)
        self.assertEqual(response.status_code, 200)
        return client, client.cookies[settings.CSRF_COOKIE_NAME].value

    def post_state(self):
        return (
            list(Post.objects.order_by('pk').values()),
            list(Post.categories.through.objects.order_by('pk').values()),
        )

    def test_unauthorized_requests_cannot_add_or_change_posts(self):
        write_permissions = ('add_post', 'change_post')
        cases = (
            ('anonymous', None, 302, (self.add_url, self.change_url)),
            ('nonstaff', self.make_user(
                'nonstaff', *write_permissions, is_staff=False,
            ), 302, (self.add_url, self.change_url)),
            ('inactive staff', self.make_user(
                'inactive', *write_permissions, is_active=False,
            ), 302, (self.add_url, self.change_url)),
            ('staff without post permissions', self.make_user('staff'), 403,
             (self.add_url, self.change_url)),
            ('view only', self.make_user('viewer', 'view_post'), 403,
             (self.add_url, self.change_url)),
            ('add only', self.make_user('creator', 'add_post'), 403,
             (self.change_url,)),
            ('change only', self.make_user('editor', 'change_post'), 403,
             (self.add_url,)),
        )
        original_state = self.post_state()
        for role, user, expected_status, urls in cases:
            client, token = self.csrf_client(user)
            for url in urls:
                with self.subTest(role=role, url=url):
                    response = client.post(
                        url, self.post_data, HTTP_X_CSRFTOKEN=token,
                    )

                    if expected_status == 302:
                        self.assertRedirects(
                            response, f"{reverse('admin:login')}?next={url}",
                            fetch_redirect_response=False,
                        )
                    else:
                        self.assertEqual(response.status_code, 403)
                        self.assertNotContains(
                            response, 'CSRF verification failed', status_code=403,
                        )
                    self.assertEqual(self.post_state(), original_state)

    def test_view_only_staff_can_read_draft_in_admin(self):
        self.client.force_login(self.make_user('viewer', 'view_post'))

        changelist = self.client.get(reverse('admin:blog_post_changelist'))
        detail = self.client.get(self.change_url)

        self.assertContains(changelist, self.draft.title)
        self.assertContains(detail, self.draft.title)
        self.assertNotContains(detail, 'name="_save"')

    def assert_saved_article(self, post):
        for field in ('title', 'slug', 'body', 'snippet', 'status'):
            self.assertEqual(getattr(post, field), self.post_data[field])
        self.assertQuerySetEqual(post.categories.all(), [self.new_category])

    def assert_author_guidance(self, response):
        form = response.context['adminform'].form
        for name, message in (
            ('body', 'The article body is rendered as trusted HTML.'),
            ('snippet', 'The snippet is rendered as trusted HTML.'),
        ):
            self.assertIn(message, form.fields[name].help_text)
            self.assertContains(response, message, count=1)
            self.assertIn(
                'Review pasted markup and link destinations before saving.',
                form.fields[name].help_text,
            )
            self.assertIn(
                'Restrict post add/change permissions to trusted site authors.',
                form.fields[name].help_text,
            )
        self.assertContains(
            response, Post._meta.get_field('snippet').help_text, count=1,
        )
        self.assertIsInstance(form.fields['body'].widget, CKEditorWidget)
        self.assertContains(response, 'ckeditor/ckeditor-init.js')
        return form

    def test_add_and_change_forms_preserve_fields_and_render_guidance_once(self):
        self.client.force_login(
            self.make_user('author', 'add_post', 'change_post'),
        )
        model_help = {
            field.name: field.help_text for field in Post._meta.fields
        }
        standard_admin = admin.ModelAdmin(Post, admin.site)
        for url in (self.add_url, self.change_url, self.add_url, self.change_url):
            with self.subTest(url=url):
                response = self.client.get(url)

                form = self.assert_author_guidance(response)
                self.assertEqual(list(form.fields), [
                    'title', 'slug', 'image', 'body', 'snippet',
                    'categories', 'status',
                ])
                for name, field in form.fields.items():
                    self.assertEqual(field.required, name not in ('image', 'body'))
                    if name not in ('body', 'snippet'):
                        standard_field = standard_admin.formfield_for_dbfield(
                            Post._meta.get_field(name), response.wsgi_request,
                        )
                        self.assertEqual(
                            field.help_text, standard_field.help_text,
                        )
        self.assertEqual(
            {field.name: field.help_text for field in Post._meta.fields},
            model_help,
        )

    def test_invalid_forms_keep_guidance_and_entered_content_without_writes(self):
        client, token = self.csrf_client(
            self.make_user('author', 'add_post', 'change_post'),
        )
        data = {**self.post_data, 'title': ''}
        original_state = self.post_state()
        for url in (self.add_url, self.change_url):
            with self.subTest(url=url):
                response = client.post(url, data, HTTP_X_CSRFTOKEN=token)

                form = self.assert_author_guidance(response)
                self.assertFormError(form, 'title', 'This field is required.')
                for name in ('slug', 'body', 'snippet'):
                    self.assertEqual(form[name].value(), data[name])
                self.assertEqual(self.post_state(), original_state)

    def test_add_only_staff_can_create_post(self):
        client, token = self.csrf_client(self.make_user('creator', 'add_post'))
        cases = ((self.post_data['body'], 1), ('', 0))
        for index, (body, status) in enumerate(cases):
            with self.subTest(body=body, status=status):
                self.post_data.update(
                    body=body, status=status, slug=f'created-article-{index}',
                )

                response = client.post(
                    self.add_url, self.post_data, HTTP_X_CSRFTOKEN=token,
                )

                self.assertEqual(response.status_code, 302)
                self.assertEqual(Post.objects.count(), index + 2)
                self.assert_saved_article(
                    Post.objects.get(slug=self.post_data['slug']),
                )

    def test_change_only_staff_can_edit_and_publish_draft(self):
        client, token = self.csrf_client(self.make_user('editor', 'change_post'))

        for body, status in ((self.post_data['body'], 1), ('', 0)):
            with self.subTest(body=body, status=status):
                self.post_data.update(body=body, status=status)

                response = client.post(
                    self.change_url, self.post_data, HTTP_X_CSRFTOKEN=token,
                )

                self.assertEqual(response.status_code, 302)
                self.assertEqual(Post.objects.count(), 1)
                self.draft.refresh_from_db()
                self.assert_saved_article(self.draft)

    def test_authorized_writes_require_valid_csrf_token(self):
        user = self.make_user('author', 'add_post', 'change_post')
        client, token = self.csrf_client(user)
        wrong_token = ('a' if token[0] != 'a' else 'b') + token[1:]
        original_state = self.post_state()
        for url in (self.add_url, self.change_url):
            for case, headers in (
                ('missing token', {}),
                ('invalid token', {'HTTP_X_CSRFTOKEN': wrong_token}),
            ):
                with self.subTest(url=url, case=case):
                    response = client.post(url, self.post_data, **headers)

                    self.assertContains(
                        response, 'CSRF verification failed', status_code=403,
                    )
                    self.assertEqual(self.post_state(), original_state)
