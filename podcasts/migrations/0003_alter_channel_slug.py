# Generated by Django 4.0 on 2021-12-20 11:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0002_alter_channel_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='slug',
            field=models.SlugField(blank=True),
        ),
    ]
