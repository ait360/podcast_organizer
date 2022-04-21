# Generated by Django 3.2.12 on 2022-03-21 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0023_auto_20220319_2024'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='listener',
            options={'ordering': ['-updated_on'], 'verbose_name': 'Listener'},
        ),
        migrations.AlterField(
            model_name='listener',
            name='time_listened',
            field=models.FloatField(blank=True, default=0.0),
        ),
    ]