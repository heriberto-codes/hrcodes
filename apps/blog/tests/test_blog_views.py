from django.test import TestCase, Client
from django.urls import reverse

class TestBlogViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.base_url = reverse('blog')
        
    def test_can_load_base_blog_template(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/base_blog.html')
        
    def test_can_load_blog_index_template(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/blog_index.html')