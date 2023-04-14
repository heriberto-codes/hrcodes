from django.test import TestCase, Client
from django.urls import reverse

class TestArchiveViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.base_url = reverse('archive')
        
    def test_can_load_base_archive_template(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'archive/base_archive.html')
        
    def test_can_load_archive_template(self):
        response = self.client.get(self.base_url)
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'archive/archive.html')
        