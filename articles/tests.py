from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from accounts.models import User, UserRole
from taxonomy.models import Category
from media_lib.models import MediaAsset
from articles.models import Article, ArticleStatus, Tag
from articles.tasks import publish_scheduled_articles

class ArticleWorkflowTests(TestCase):

    def setUp(self):
        self.author = User.objects.create_user(username='reporter1', email='reporter1@example.com', password='pass', role=UserRole.AUTHOR)
        self.category = Category.objects.create(name='Tech', slug='tech')
        self.media_without_alt = MediaAsset.objects.create(title='Server Room', alt_text='')
        self.media_with_alt = MediaAsset.objects.create(title='Data Center', alt_text='A modern high speed data center server rack')

    def test_article_creation_and_revisions(self):
        article = Article.objects.create(
            title='Quantum Computing Milestone Achieved',
            summary='Researchers announce a breakthrough in qubit stability.',
            content='Full detailed article body text here...',
            primary_category=self.category,
            author=self.author,
            status=ArticleStatus.DRAFT
        )
        self.assertEqual(article.slug, 'quantum-computing-milestone-achieved')
        self.assertEqual(article.revisions.count(), 1)
        self.assertEqual(article.revisions.first().version_number, 1)

    def test_alt_text_validation_on_publish(self):
        article = Article.objects.create(
            title='AI Advances in Healthcare',
            summary='New diagnostic tools deployed.',
            content='Body text for AI story...',
            primary_category=self.category,
            author=self.author,
            main_image=self.media_without_alt,
            status=ArticleStatus.PUBLISHED
        )
        with self.assertRaises(ValidationError):
            article.clean()

    def test_successful_publication_with_alt_text(self):
        article = Article.objects.create(
            title='Renewable Energy Record Broken',
            summary='Solar power output reaches peak.',
            content='Body text for green energy...',
            primary_category=self.category,
            author=self.author,
            main_image=self.media_with_alt,
            status=ArticleStatus.PUBLISHED
        )
        # Should clean without error
        article.clean()
        self.assertIsNotNone(article.published_at)

    def test_celery_scheduled_publishing_task(self):
        scheduled_time = timezone.now() - timezone.timedelta(minutes=5)
        article = Article.objects.create(
            title='Scheduled Breaking News',
            summary='Timed dispatch story.',
            content='Body content here...',
            primary_category=self.category,
            author=self.author,
            status=ArticleStatus.DRAFT,
            scheduled_at=scheduled_time
        )
        result = publish_scheduled_articles()
        article.refresh_from_db()
        self.assertEqual(article.status, ArticleStatus.PUBLISHED)
        self.assertIn('Successfully published 1', result)
