from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from apps.blog.models import Post, Comment, Category

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
        
        expected_url = reverse('blog_detail', kwargs={'slug': self.post.slug})
        
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
        