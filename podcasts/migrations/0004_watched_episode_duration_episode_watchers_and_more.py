# Generated by Django 4.0 on 2022-02-04 20:31

import ckeditor_uploader.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('podcasts', '0003_alter_channel_slug'),
    ]

    operations = [
        migrations.CreateModel(
            name='Watched',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_watched', models.PositiveBigIntegerField(blank=True)),
                ('watched', models.BooleanField(blank=True)),
                ('created_on', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('updated_on', models.DateTimeField(auto_now=True, verbose_name='date updated')),
            ],
        ),
        migrations.AddField(
            model_name='episode',
            name='duration',
            field=models.PositiveBigIntegerField(default=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='episode',
            name='watchers',
            field=models.ManyToManyField(related_name='watched', through='podcasts.Watched', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='channel',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True),
        ),
        migrations.AddField(
            model_name='watched',
            name='episode',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='epi_watched', to='podcasts.episode'),
        ),
        migrations.AddField(
            model_name='watched',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_watched', to='users.user'),
        ),
    ]
