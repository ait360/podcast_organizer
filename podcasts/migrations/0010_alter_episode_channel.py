# Generated by Django 4.0.2 on 2022-02-11 15:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('podcasts', '0009_alter_episode_number_alter_episode_season'),
    ]

    operations = [
        migrations.AlterField(
            model_name='episode',
            name='channel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episodes', to='podcasts.channel'),
        ),
    ]
