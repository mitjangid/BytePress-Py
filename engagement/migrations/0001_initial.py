import uuid
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('articles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(db_index=True, max_length=254, unique=True, verbose_name='email address')),
                ('is_active', models.BooleanField(default=True, verbose_name='is active')),
                ('token', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='unsubscribe token')),
                ('subscribed_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Newsletter Subscriber',
                'verbose_name_plural': 'Newsletter Subscribers',
                'ordering': ['-subscribed_at'],
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author_name', models.CharField(blank=True, max_length=100, verbose_name='author name')),
                ('author_email', models.EmailField(blank=True, max_length=254, verbose_name='author email')),
                ('content', models.TextField(verbose_name='comment content')),
                ('status', models.CharField(choices=[('PENDING', 'Pending Moderation'), ('APPROVED', 'Approved'), ('FLAGGED', 'Flagged Spam'), ('REJECTED', 'Rejected')], db_index=True, default='PENDING', max_length=15, verbose_name='status')),
                ('ip_address', models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address')),
                ('user_agent', models.TextField(blank=True, verbose_name='User-Agent')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='articles.article')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='engagement.comment')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comments', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Comment',
                'verbose_name_plural': 'Comments',
                'ordering': ['created_at'],
            },
        ),
        migrations.CreateModel(
            name='NewsletterDigest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='subject line')),
                ('status', models.CharField(choices=[('DRAFT', 'Draft'), ('SENDING', 'Sending'), ('SENT', 'Sent')], default='DRAFT', max_length=15, verbose_name='status')),
                ('scheduled_for', models.DateTimeField(verbose_name='scheduled send time')),
                ('sent_at', models.DateTimeField(blank=True, null=True, verbose_name='sent at')),
                ('articles', models.ManyToManyField(related_name='newsletter_digests', to='articles.article')),
            ],
            options={
                'verbose_name': 'Newsletter Digest',
                'verbose_name_plural': 'Newsletter Digests',
                'ordering': ['-scheduled_for'],
            },
        ),
        migrations.CreateModel(
            name='WebPushSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('endpoint', models.URLField(max_length=500, verbose_name='push endpoint')),
                ('p256dh', models.CharField(max_length=255, verbose_name='p256dh key')),
                ('auth', models.CharField(max_length=255, verbose_name='auth key')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='push_subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Web Push Subscription',
                'verbose_name_plural': 'Web Push Subscriptions',
            },
        ),
        migrations.CreateModel(
            name='Bookmark',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarked_by', to='articles.article')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bookmark',
                'verbose_name_plural': 'Bookmarks',
                'ordering': ['-created_at'],
                'unique_together': {('user', 'article')},
            },
        ),
    ]
