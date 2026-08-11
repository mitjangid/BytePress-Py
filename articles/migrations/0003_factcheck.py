from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_article_content_hi_article_summary_hi_article_title_hi'),
    ]

    operations = [
        migrations.CreateModel(
            name='FactCheck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('claim_text', models.CharField(help_text='Viral statement or post being verified.', max_length=255, verbose_name='claim text')),
                ('claim_by', models.CharField(default='Social Media / Viral Forward', max_length=150, verbose_name='claimed by')),
                ('verdict', models.CharField(choices=[('TRUE', 'सत्य / True'), ('FALSE', 'असत्य / False'), ('MISLEADING', 'भ्रामक / Misleading')], default='FALSE', max_length=20, verbose_name='verdict')),
                ('explanation', models.TextField(help_text='Detailed reasoning behind the rating verdict.', verbose_name='fact check explanation')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('article', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fact_check', to='articles.article')),
            ],
            options={
                'verbose_name': 'Fact Check Verification',
                'verbose_name_plural': 'Fact Check Verifications',
            },
        ),
    ]
