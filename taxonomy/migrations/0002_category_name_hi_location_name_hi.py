from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('taxonomy', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name_hi',
            field=models.CharField(blank=True, help_text='e.g. तकनीक, राजनीति, खेल', max_length=100, verbose_name='category name (Hindi / Regional)'),
        ),
        migrations.AddField(
            model_name='location',
            name='name_hi',
            field=models.CharField(blank=True, help_text='e.g. दिल्ली, मुंबई, उत्तर प्रदेश', max_length=100, verbose_name='location name (Hindi / Regional)'),
        ),
    ]
