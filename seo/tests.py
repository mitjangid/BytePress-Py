from django.test import TestCase, Client
from seo.models import Redirect

class SEOTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.redirect = Redirect.objects.create(
            old_path='/old-article-slug/',
            new_path='/article/quantum-computing-milestone-achieved/'
        )

    def test_redirect_middleware(self):
        response = self.client.get('/old-article-slug/')
        self.assertEqual(response.status_code, 301)
        self.assertEqual(response.url, '/article/quantum-computing-milestone-achieved/')

    def test_robots_txt_view(self):
        response = self.client.get('/robots.txt')
        self.assertEqual(response.status_code, 200)
        self.assertIn('User-agent: *', response.content.decode())
