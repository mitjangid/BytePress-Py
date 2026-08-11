from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('media_lib', '0001_initial'),
        ('taxonomy', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='tag name')),
                ('slug', models.SlugField(max_length=60, unique=True, verbose_name='slug')),
            ],
            options={
                'verbose_name': 'Tag',
                'verbose_name_plural': 'Tags',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='slug')),
                ('summary', models.TextField(help_text='Short deck summary used on cards & meta description fallback.', max_length=500, verbose_name='summary / dek')),
                ('content', models.TextField(help_text='Rich text body content.', verbose_name='article content')),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PUBLISHED', 'Published'), ('ARCHIVED', 'Archived')], db_index=True, default='DRAFT', max_length=20, verbose_name='status')),
                ('published_at', models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='published at')),
                ('scheduled_at', models.DateTimeField(blank=True, help_text='Timestamp for automated scheduled publishing via Celery Beat.', null=True, verbose_name='scheduled publishing time')),
                ('is_breaking', models.BooleanField(db_index=True, default=False, verbose_name='is breaking news')),
                ('is_featured', models.BooleanField(db_index=True, default=False, verbose_name='is featured story')),
                ('is_trending', models.BooleanField(db_index=True, default=False, verbose_name='is trending story')),
                ('is_editors_pick', models.BooleanField(db_index=True, default=False, verbose_name="is editor's pick")),
                ('views_count', models.PositiveIntegerField(default=0, verbose_name='views count')),
                ('reading_time_minutes', models.PositiveIntegerField(default=1, verbose_name='reading time (minutes)')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='authored_articles', to=settings.AUTH_USER_MODEL, verbose_name='primary author')),
                ('co_authors', models.ManyToManyField(blank=True, related_name='co_authored_articles', to=settings.AUTH_USER_MODEL, verbose_name='co-authors')),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='articles', to='taxonomy.location', verbose_name='news location')),
                ('main_image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='featured_in_articles', to='media_lib.mediaasset', verbose_name='main featured image')),
                ('primary_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='primary_articles', to='taxonomy.category', verbose_name='primary category')),
                ('secondary_categories', models.ManyToManyField(blank=True, related_name='secondary_articles', to='taxonomy.category', verbose_name='secondary categories')),
                ('tags', models.ManyToManyField(blank=True, related_name='articles', to='articles.tag', verbose_name='tags')),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
                'ordering': ['-published_at', '-created_at'],
                'permissions': [('can_publish_article', 'Can approve and publish articles'), ('can_manage_featured', 'Can flag breaking and featured news')],
            },
        ),
        migrations.CreateModel(
            name='ArticleRevision',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('version_number', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=255)),
                ('summary', models.TextField()),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='revisions', to='articles.article')),
                ('edited_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Article Revision',
                'verbose_name_plural': 'Article Revisions',
                'ordering': ['-version_number'],
            },
        ),
        migrations.CreateModel(
            name='ArticleStateLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('from_state', models.CharField(choices=[('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PUBLISHED', 'Published'), ('ARCHIVED', 'Archived')], max_length=20)),
                ('to_state', models.CharField(choices=[('DRAFT', 'Draft'), ('PENDING_REVIEW', 'Pending Review'), ('PUBLISHED', 'Published'), ('ARCHIVED', 'Archived')], max_length=20)),
                ('notes', models.TextField(blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state_logs', to='articles.article')),
                ('changed_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Article State Log',
                'verbose_name_plural': 'Article State Logs',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='RelatedArticleOverride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.PositiveIntegerField(default=1)),
                ('source_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manual_related_sources', to='articles.article')),
                ('target_article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manual_related_targets', to='articles.article')),
            ],
            options={
                'verbose_name': 'Related Article Override',
                'verbose_name_plural': 'Related Article Overrides',
                'ordering': ['position'],
                'unique_together': {('source_article', 'target_article')},
            },
        ),
    ]
