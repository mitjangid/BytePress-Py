from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('seo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortenedURL',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('short_code', models.CharField(db_index=True, max_length=12, unique=True, verbose_name='short code')),
                ('target_url', models.CharField(db_index=True, max_length=500, verbose_name='target URL or path')),
                ('click_count', models.PositiveIntegerField(default=0, verbose_name='clicks count')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Shortened URL',
                'verbose_name_plural': 'Shortened URLs',
                'ordering': ['-created_at'],
            },
        ),
    ]
