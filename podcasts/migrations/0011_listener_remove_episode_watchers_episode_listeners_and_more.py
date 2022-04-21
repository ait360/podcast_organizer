# Generated by Django 4.0.2 on 2022-02-11 22:48

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0003_alter_profile_user'),
        ('podcasts', '0010_alter_episode_channel'),
    ]

    operations = [
        migrations.CreateModel(
            name='Listener',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_watched', models.FloatField(blank=True)),
                ('watched', models.BooleanField(blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
        ),
        migrations.RemoveField(
            model_name='episode',
            name='watchers',
        ),
        migrations.AddField(
            model_name='episode',
            name='listeners',
            field=models.ManyToManyField(related_name='listeners', through='podcasts.Listener', to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Watched',
        ),
        migrations.AddField(
            model_name='listener',
            name='episode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='episode_listener', to='podcasts.episode'),
        ),
        migrations.AddField(
            model_name='listener',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_listener', to=settings.AUTH_USER_MODEL),
        ),
    ]