from urllib import response
from django.test import TestCase, Client
from django.urls import reverse

# Create your tests here.
class TestViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.base_url = reverse('home')  
            
    def test_can_view_base_template(self):
        
        response = self.client.get(self.base_url)
        
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'home.html')
        