from django.db import migrations, models

class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Redirect',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_path', models.CharField(db_index=True, help_text="e.g. '/news/old-article-slug/'", max_length=255, unique=True, verbose_name='old URL path')),
                ('new_path', models.CharField(help_text="e.g. '/news/new-article-slug/'", max_length=255, verbose_name='new URL path')),
                ('redirect_type', models.IntegerField(choices=[(301, '301 Permanent Redirect'), (302, '302 Temporary Redirect')], default=301, verbose_name='redirect HTTP status')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hits_count', models.PositiveIntegerField(default=0, verbose_name='redirect hits count')),
            ],
            options={
                'verbose_name': '301 Redirect',
                'verbose_name_plural': '301 Redirects',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='SEOOverride',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('canonical_url', models.URLField(blank=True, verbose_name='canonical URL')),
                ('og_title', models.CharField(blank=True, max_length=255, verbose_name='OpenGraph title')),
                ('og_description', models.TextField(blank=True, verbose_name='OpenGraph description')),
                ('og_image', models.URLField(blank=True, verbose_name='OpenGraph image URL')),
                ('no_index', models.BooleanField(default=False, verbose_name='noindex robots tag')),
                ('schema_type', models.CharField(default='NewsArticle', max_length=50, verbose_name='Schema.org type')),
            ],
            options={
                'verbose_name': 'SEO Meta Override',
                'verbose_name_plural': 'SEO Meta Overrides',
            },
        ),
    ]
