# Generated by Django 3.2.12 on 2022-03-19 19:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0022_alter_listener_streams'),
    ]

    operations = [
        migrations.AddField(
            model_name='listener',
            name='completed_count',
            field=models.IntegerField(blank=True, default=0),
        ),
        migrations.AddField(
            model_name='listener',
            name='start_time',
            field=models.FloatField(blank=True, default=0),
        ),
    ]
