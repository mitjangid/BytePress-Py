from django.test import TestCase, Client
from accounts.models import User, UserRole
from taxonomy.models import Category
from articles.models import Article, ArticleStatus
from engagement.models import Comment, Bookmark, NewsletterSubscriber, CommentStatus

class EngagementTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='reader_john', email='john@example.com', password='password123')
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.article = Article.objects.create(
            title='Tech News Article',
            summary='Summary deck text',
            content='Full content text...',
            primary_category=self.category,
            author=self.user,
            status=ArticleStatus.PUBLISHED
        )

    def test_post_comment_authenticated(self):
        self.client.login(username='reader_john', password='password123')
        response = self.client.post(
            f'/comment/post/{self.article.slug}/',
            {'content': 'Great article!'},
            HTTP_HX_REQUEST='true'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(Comment.objects.first().status, CommentStatus.APPROVED)

    def test_toggle_bookmark(self):
        self.client.login(username='reader_john', password='password123')
        response = self.client.post(f'/bookmark/toggle/{self.article.slug}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Bookmark.objects.count(), 1)

    def test_newsletter_subscribe(self):
        response = self.client.post('/newsletter/subscribe/', {'email': 'new_reader@example.com'})
        self.assertEqual(response.status_code, 302)
        self.assertEqual(NewsletterSubscriber.objects.count(), 1)
