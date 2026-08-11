from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='content_hi',
            field=models.TextField(blank=True, verbose_name='Hindi / Regional Article Content'),
        ),
        migrations.AddField(
            model_name='article',
            name='summary_hi',
            field=models.TextField(blank=True, max_length=500, verbose_name='Hindi / Regional Summary'),
        ),
        migrations.AddField(
            model_name='article',
            name='title_hi',
            field=models.CharField(blank=True, help_text='Hindi translation of article title.', max_length=255, verbose_name='Hindi / Regional Title'),
        ),
    ]
