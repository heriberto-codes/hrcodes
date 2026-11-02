from django.contrib import admin
from django.test import RequestFactory, TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from apps.blog.models import Post


class TestPublishedPostQuerySet(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.first_published = Post.objects.create(
            title='Selected first', slug='selected-a', snippet='First.',
            status=1,
        )
        cls.second_published = Post.objects.create(
            title='Selected second', slug='selected-b', snippet='Second.',
            status=1,
        )
        cls.other_published = Post.objects.create(
            title='Other published', slug='other', snippet='Other.',
            status=1,
        )
        cls.draft = Post.objects.create(
            title='Selected draft', slug='selected-draft', snippet='Draft.',
            status=0,
        )
        cls.unsupported = Post.objects.create(
            title='Selected unsupported', slug='selected-unsupported',
            snippet='Unsupported status.', status=2,
        )
        cls.all_posts = [
            cls.first_published, cls.second_published, cls.other_published,
            cls.draft, cls.unsupported,
        ]

    def test_published_returns_only_exact_published_status_without_writes(self):
        statuses_before = dict(Post.objects.values_list('pk', 'status'))

        self.assertQuerySetEqual(
            Post.objects.published(),
            [self.first_published, self.second_published, self.other_published],
            ordered=False,
        )

        self.assertEqual(
            dict(Post.objects.values_list('pk', 'status')), statuses_before,
        )

    def test_published_composes_with_filters_and_preserves_ordering(self):
        querysets = (
            Post.objects.filter(title__startswith='Selected')
            .published().order_by('-slug'),
            Post.objects.published()
            .filter(title__startswith='Selected').order_by('-slug'),
            Post.objects.filter(title__startswith='Selected')
            .order_by('-slug').published(),
        )

        for index, queryset in enumerate(querysets):
            with self.subTest(chain=index):
                self.assertQuerySetEqual(
                    queryset, [self.second_published, self.first_published],
                )

    def test_published_handles_empty_and_unpublished_only_querysets(self):
        querysets = (
            Post.objects.none().published(),
            Post.objects.filter(
                pk__in=[self.draft.pk, self.unsupported.pk],
            ).published(),
        )

        for index, queryset in enumerate(querysets):
            with self.subTest(case=index):
                self.assertQuerySetEqual(queryset, [])

    def test_ordinary_default_and_base_managers_keep_all_posts_visible(self):
        for manager in (
            Post.objects, Post._default_manager, Post._base_manager,
        ):
            with self.subTest(manager=manager.name):
                self.assertQuerySetEqual(
                    manager.all(), self.all_posts, ordered=False,
                )

    def test_registered_admin_queryset_keeps_drafts_visible(self):
        request = RequestFactory().get(reverse('admin:blog_post_changelist'))
        post_admin = admin.site.get_model_admin(Post)

        self.assertQuerySetEqual(
            post_admin.get_queryset(request), self.all_posts, ordered=False,
        )


class TestBlogPost(TestCase):
    def setUp(self) -> None:
        self.post = Post.objects.create(
            title='My first job as a SWE',
            body='This is great getting paid to code',
            slug='first-swe-job',
        )
        
        self.image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'binary_content_of_the_image',
            content_type='image/jpeg'
        )
        
        self.post_with_image = Post.objects.create(
            title='Post with image',
            body='This post has an image',
            slug='postWithImage',
            image=self.image_file
        )
    
    def tearDown(self):
        self.image_file.close()
        self.post.delete()
        self.post_with_image.delete()
        
    def test_post_title(self):
        self.assertEqual(self.post.title, 'My first job as a SWE')
    
    def test_post_body(self):
        self.assertEqual(self.post.body, 'This is great getting paid to code')
    
    def test_post_slug(self):
        self.assertEqual(self.post.slug, 'first-swe-job')
        
    def test_image_field(self):
        self.assertIsNotNone(self.post.image)
        self.assertIn('.jpg', self.post_with_image.image.name)
        
    def test_get_absolute_url(self):
        returned_url = self.post.get_absolute_url()
        
        expected_url = reverse(
            'blog_detail',
            kwargs={'pk': self.post.pk, 'slug': self.post.slug},
        )
        
        self.assertEqual(returned_url, expected_url)
        
        
# class TestCategory(TestCase):
#     def test_return_name(self):
#         category = Category(name='Test Category')
#         returned_name = str(category)
#         self.assertEqual(returned_name, category.name)
        
#     def test_get_absolute_url(self):
#         # create the category instance 
#         category = Category.objects.create(name='blog_category', slug='test-category')
        
#         # call the get absolute url() method 
#         returned_url = category.get_absolute_url()

#         # generate the expected URL using reverse()
#         expected_url = reverse('Test Category', kwargs={'slug': 'test-category'})
        
#         # make the assertion 
#         self.assertEqual(returned_url, expected_url)
