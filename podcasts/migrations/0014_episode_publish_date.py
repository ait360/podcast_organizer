# Generated by Django 4.0.2 on 2022-02-16 22:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0013_rename_dislike_episode_dislikes'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='publish_date',
            field=models.DateTimeField(blank=True, default=None, null=True),
        ),
    ]