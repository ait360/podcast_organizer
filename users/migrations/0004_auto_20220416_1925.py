# Generated by Django 3.2.12 on 2022-04-16 18:25

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='website',
            field=models.URLField(help_text='eg https://www.podcast.com', max_length=250),
        ),
        migrations.AlterField(
            model_name='user',
            name='cover_picture',
            field=models.ImageField(default='cover_picture.jpeg', upload_to=users.models.user_cover_path),
        ),
        migrations.AlterField(
            model_name='user',
            name='display_picture',
            field=models.ImageField(default='default_profile.png', upload_to=users.models.user_directory_path),
        ),
    ]
