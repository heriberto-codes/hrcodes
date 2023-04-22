from django.test import TestCase, Client
from django.urls import reverse

class TestBlogViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.base_url = reverse('blog_index')
        self.blog_detail_url = reverse('blog_detail', kwargs={'pk': 1, 'slug': 'test'})
        self.blog_category_url = reverse('blog_category', kwargs={'category': 'category'})
        
    def test_can_load_base_blog_template(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/base_blog.html')
        
    def test_can_load_blog_index_template(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_index.html')
          
    def test_can_load_blog_detail_template(self):
        response = self.client.get(self.blog_detail_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_can_load_blog_category(self):
        response = self.client.get(self.blog_category_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_category.html')
