from django.test import TestCase, Client
from django.templatetags.static import static
from django.urls import reverse

class TestArchiveViews(TestCase):
    def setUp(self) -> None:
        self.client = Client()
        self.base_url = reverse('archive')
        
    def test_can_load_base_archive_template(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'archive/base_archive.html')
        
    def test_can_load_archive_template(self):
        response = self.client.get(self.base_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'archive/archive.html')

    def test_archive_keeps_non_home_page_scope(self):
        response = self.client.get(self.base_url)

        self.assertContains(response, '<body class="hrBody">')
        self.assertNotContains(response, 'class="hrBody home-page"')
        self.assertNotContains(
            response,
            f'href="{static("pages/home.css")}"',
        )
