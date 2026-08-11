from django.test import TestCase, Client
from accounts.models import User
from taxonomy.models import Category
from articles.models import Article, ArticleStatus

class CoreViewsTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='author1', email='author1@example.com', password='pass')
        self.category = Category.objects.create(name='Business', slug='business')
        self.article = Article.objects.create(
            title='Business Growth Report',
            summary='Economic summary text',
            content='Detailed financial content body...',
            primary_category=self.category,
            author=self.user,
            status=ArticleStatus.PUBLISHED
        )

    def test_homepage_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Headlines')

    def test_article_detail_view(self):
        response = self.client.get(f'/article/{self.article.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Business Growth Report')

    def test_search_view(self):
        response = self.client.get('/search/?q=Business')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Business Growth Report')
