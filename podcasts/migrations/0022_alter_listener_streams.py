# Generated by Django 3.2.12 on 2022-03-08 22:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0021_rename_time_watched_listener_time_listened'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listener',
            name='streams',
            field=models.IntegerField(blank=True, default=0),
        ),
    ]
