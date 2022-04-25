from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError



from phonenumber_field.modelfields import PhoneNumberField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='profile')
    name = models.CharField(max_length=200, )
    bio = models.TextField()
    website = models.URLField(max_length=250, blank=True, help_text=_('eg https://www.podcast.com'))
    phone_number = PhoneNumberField(blank=True)
    slug = models.SlugField(max_length=150, unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('user_urls:profile_detail', kwargs={'username': self.slug})

    def get_update_url(self):
        return reverse('user_urls:profile_update', kwargs={'username': self.slug})

    def get_public_profile_url(self):
        return reverse('user_urls:public_profile', kwargs={'username': self.slug})


class UserManger(BaseUserManager):
    use_in_migrations = True


    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError('Input a username, I need it to set up your account')
        email = self.normalize_email(email)
        # access the model the manager is attached to via self.model attribute
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)

    def get_by_natural_key(self, username):
        case_insensitive_username_field = f'{self.model.USERNAME_FIELD}__iexact'
        return self.get(**{case_insensitive_username_field: username})

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.username, filename)


def user_cover_path(instance, filename):
    return 'user_cover_{0}/{1}'.format(instance.username, filename)

def validate_profile_slug(value):

    if not User.objects.filter(username__iexact=value).exists():

        if Profile.objects.filter(slug__iexact=slugify(value)).exists():
            raise ValidationError(_("A user with that username already exists."))

class User(AbstractBaseUser, PermissionsMixin):

    username_validator = UnicodeUsernameValidator()

    username = models.CharField(
        _('username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator, validate_profile_slug],
        error_messages={
            'unique': _("A user with that username already exists."),
        },
    )
    email = models.EmailField(_('email address'), blank=False, unique=True)
    display_picture = models.ImageField(upload_to=user_directory_path, default='default_profile.png' )
    cover_picture = models.ImageField(upload_to=user_cover_path, default='cover_picture.jpeg')
    date_joined = models.DateTimeField(_('date joined'), auto_now_add=True)
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
        help_text=_('Designates whether the users can log into this admin site')
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
        help_text=_(
            'Designates whether this users should be treated as active. '
            'Unselect this instead of deleting account'
        )
    )

    objects = UserManger()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = _('users')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        pass



    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this users."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.update_or_create(user=instance,
                                         defaults={'slug': slugify(
                                                  instance.get_username()),})

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()