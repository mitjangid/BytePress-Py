from django.test import TestCase, Client
from accounts.models import User
from taxonomy.models import Category
from articles.models import Article, ArticleStatus

class APITests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='api_author', email='api@example.com', password='pass')
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.article = Article.objects.create(
            title='API Test Story',
            summary='API summary',
            content='API body content...',
            primary_category=self.category,
            author=self.user,
            status=ArticleStatus.PUBLISHED
        )

    def test_article_list_api(self):
        response = self.client.get('/api/v1/articles/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('results', data)
        self.assertEqual(len(data['results']), 1)

    def test_article_detail_api(self):
        response = self.client.get(f'/api/v1/articles/{self.article.slug}/')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['title'], 'API Test Story')
