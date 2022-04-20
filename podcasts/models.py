import uuid
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from django.core.validators import FileExtensionValidator, URLValidator, EmailValidator
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.db.models.signals import post_save
from django.urls import reverse
from django.dispatch import receiver
from django.utils.text import slugify
from django.utils import timezone

#from django_ckeditor_5.fields import CKEditor5Field
from ckeditor_uploader.fields import RichTextUploadingField



# Create your models here.

def channel_cover_path(instance, filename):
    filename = '_'.join(filename.split())
    channel_name= '_'.join(instance.name.split())
    return f'channel_cover_{channel_name}/{filename}'

def channel_display_path(instance, filename):
    filename = '_'.join(filename.split())
    channel_name = '_'.join(instance.name.split())
    return f'channel_display_{channel_name}/{filename}'


class Channel(models.Model):
    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required for your channels url. 150 characters or fewer.\
                    Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _("A users with that username already exists."),
        },
    )
    name = models.CharField(_('channel name'), max_length=200)
    description = RichTextUploadingField(blank=True)
    #description = models.TextField(_('channel descriptions'), blank=False)
    website = models.URLField(_('webiste'), validators=[URLValidator()],
                              blank=True,
                              help_text=_('add your website to allow your \
                              subscribesrs know more about you \
                                          eg https://www.podcast.com'))
    email = models.EmailField(_('email address'), blank=False,
                        validators=[EmailValidator()],
                        help_text=_('add your email address to allow your \
                                    subscribers reach you'))
    display_picture = models.ImageField(_('display picture'),
                                        upload_to=channel_display_path,
                                        default='channel_picture.jpg')
    cover_picture = models.ImageField(_('cover picture'),
                                      upload_to=channel_cover_path,
                                      default='cover_picture.jpeg')
    hosts = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='channels')
    subscribers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                         related_name='subscribers',
                                         through='Subscriber')
    explicit = models.BooleanField(_('family friendly ? '))
    slug = models.SlugField(blank=True)
    created_on = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_on = models.DateTimeField(_('date updated'), auto_now=True)

    class Meta:
        ordering = ['-created_on']
        verbose_name = 'channels'
        verbose_name_plural = 'Channels'

    def __str__(self):
        return f'{self.name}@{self.username}'

    def get_create_url(self):
        return reverse('channel_urls:channel_create')

    def get_episode_create_url(self):
        return reverse('channel_urls:episode_create', kwargs={'slug': self.slug})

    def get_absolute_url(self):
        return reverse('channel_urls:channel_detail', kwargs={'slug': self.slug})

    def get_delete_url(self):
        return reverse('channel_urls:channel_delete', kwargs={'slug': self.slug})

    def get_update_url(self):
        return reverse('channel_urls:channel_update', kwargs={'slug': self.slug})

    def get_episodes_list_url(self):
        return reverse('channel_urls:channel_episodes', kwargs={'slug': self.slug})

    def get_subscribe_url(self):
        return reverse('channel_urls:channel_subscribe', kwargs={'slug': self.slug})

    def get_subscribers_count(self):
        return self.subscribers.all().count()

    # def save(self, *args, **kwargs):
    #     self.slug = slugify(self.username)
    #     super(Channel, self).save(*args, **kwargs)

def episode_path(instance, filename):
    filename = '_'.join(filename.split())
    channel_name = '_'.join(instance.channel.name.split())
    return f'episode_{channel_name}/{filename}'

def episode_image_path(instance, filename):
    filename = ''.join(filename.split())
    channel_name = '_'.join(instance.channel.name.split())
    return f'episode_image{channel_name}/{filename}'


class Episode(models.Model):
    EPISODE_TYPE = [
        ('full', 'full'),
        ('bonus', 'bonus'),
        ('trailer', 'trailer')
    ]
    PUBLISH_STATUS = [
        ('Draft', 'Draft'),
        ('Published', 'Published'),
        ('Withdrawn', 'Withdrawn'),
        ('Pending', 'Pending'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_('Episode title'), max_length=250, blank=False,)
    image = models.ImageField(_('episode image'), upload_to=episode_image_path, blank=True)
    season = models.IntegerField(_('Season number'), blank=True, null=True)
    number = models.IntegerField(_('Episode number'), blank=True, null=True)
    description = RichTextUploadingField(blank=True, null=True)
    kind = models.CharField(_('Episode type'), choices=EPISODE_TYPE,
                             max_length=7,
                             help_text=_('full, bonus, trailer'),
                             blank=True)
    episode = models.FileField(_('Episode Audio'),
                               upload_to=episode_path,
                               validators=[FileExtensionValidator(['mp3'])],
                               help_text=_('it should be a mp3 file'),
                               error_messages={
                                   'invalid': _("your file format is unsupported"),
                               },
                               blank=True)
    duration = models.FloatField(blank=True)
    explicit = models.BooleanField(_('family friendly ? '))
    status = models.CharField(_('Publish Status'), choices=PUBLISH_STATUS,
                            max_length=9,
                            help_text=_('draft, published, withdrawn'),)
    guest = models.CharField(max_length=300, blank=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='likes',
                                   through='Like')
    dislikes = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                   related_name='dislikes',
                                   through='Dislike')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                                related_name='episodes')
    listeners = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                     related_name='listeners',
                                     through='Listener')
    publish_date = models.DateTimeField(_('date published'), blank=True, null=True, default=None)
    created_on = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_on = models.DateTimeField(_('date updated'), auto_now=True)


    class Meta:
        ordering = ['-created_on']
        verbose_name = 'Episode'
        verbose_name_plural = 'Episodes'

    def __str__(self):
        return f'{self.title}-episode{self.number}'

    def get_absolute_url(self):
        return reverse('episode_urls:episode_detail', kwargs={'id': self.id})

    def get_like_url(self):
        return reverse('episode_urls:episode_like', kwargs={'id': self.id})

    def get_dislike_url(self):
        return reverse('episode_urls:episode_dislike', kwargs={'id': self.id})

    def get_publish_url(self):
        return reverse('episode_urls:episode_publish_now', kwargs={'id': self.id})

    def get_publish_later_url(self):
        return reverse('episode_urls:episode_publish_later', kwargs={'id': self.id})

    def get_paused_url(self):
        return reverse('episode_urls:episode_paused', kwargs={'id': self.id})

    def get_download_url(self):
        return reverse('episode_urls:episode_download', kwargs={'id': self.id})

    def get_like_count(self):
        return self.likes.all().count()

    def get_dislike_count(self):
        return self.dislikes.all().count()

    def is_publised(self):
        return self.publish_date <= timezone.now()






class Like(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user_likes')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE,
                                related_name='epi_likes')
    liked = models.BooleanField()
    created_on = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_on = models.DateTimeField(_('date updated'), auto_now=True)

class Dislike(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user_dislikes')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE,
                                related_name='epi_dislikes')
    disliked = models.BooleanField()
    created_on = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_on = models.DateTimeField(_('date updated'), auto_now=True)



class Listener(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user_listener')
    episode = models.ForeignKey(Episode, on_delete=models.CASCADE,
                                related_name='episode_listener')
    time_listened = models.FloatField(blank=True, default=0.0)
    listened = models.BooleanField(blank=True, default=False)
    streams = models.IntegerField(blank=True, default=0)
    start_time = models.FloatField(blank=True, null=False, default=0)
    completed_count = models.IntegerField(blank=True, null=False, default=0)
    created_on = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_on = models.DateTimeField(_('date updated'), auto_now=True)

    class Meta:
        ordering = ['-updated_on']
        verbose_name = 'Listener'
        # verbose_name_plural = 'Listeners'

class Subscriber(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='user_subscribers')
    channel = models.ForeignKey(Channel, on_delete=models.CASCADE,
                                related_name='chn_subscribers')
    subscribed = models.BooleanField()
    created_on = models.DateTimeField(_('date created'), auto_now_add=True)
    updated_on = models.DateTimeField(_('date updated'), auto_now=True)




# @receiver(post_save, sender=Channel)
# def create_(sender, instance, created, **kwargs):
#     if created:
#         Profile.objects.update_or_create(user=instance,
#                                          defaults={'slug': slugify(
#                                                   instance.get_username()),})
#
# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()







