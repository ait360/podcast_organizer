# Generated by Django 3.2.12 on 2022-03-04 15:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0017_alter_episode_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='episode',
            name='current_time',
            field=models.FloatField(blank=True, null=True),
        ),
    ]