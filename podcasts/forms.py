import json
from pprint import pprint
from .models import Channel, Episode, Like, Subscriber, Listener
from django import forms
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, get_user
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from bootstrap_datepicker_plus.widgets import DateTimePickerInput, TimePickerInput, DatePickerInput
from django_celery_beat.models import ClockedSchedule, PeriodicTask, IntervalSchedule

validate_username = UnicodeUsernameValidator()


class MultiUsernameField(forms.Field):
    def to_python(self, value):
        if not value:
            return []
        return [i.strip() for i in value.split(',') if i]

    def validate(self, value):

        super().validate(value)
        for username in value:
            validate_username(username)


class ChannelForm(forms.ModelForm):
    co_host = MultiUsernameField(required=False, label=_('Co Hosts'),
                                 help_text=_('Add Co hosts of the channel \
                                 via their username separated with commas'))

    class Meta:
        model = Channel
        fields = ['username', 'name', 'description', 'email', 'website',
                  'cover_picture', 'display_picture', 'explicit']

    def clean_co_host(self):
        username_list = self.cleaned_data['co_host']
        user = get_user_model()
        if username_list:
            for username in username_list:
                if not user.objects.filter(username__iexact=username).exists():
                    return ValidationError(f"{username} does not exist")

        return username_list

    # def clean_display_picture(self):
    #     display_picture = self.cleaned_data['display_picture']
    #
    #     print(display_picture)
    #     raise ValidationError('just checking stuffs')

    def save(self, request, commit=True):
        channel = super().save(commit=False)
        if not channel.pk:
            channel.slug = slugify(channel.username)

        user = get_user_model()
        username_list = self.cleaned_data['co_host']

        co_host_objects = [get_user(request)] + list(
            user.objects.filter(username__in=username_list))
        if commit:
            channel.save()
            channel.hosts.set(co_host_objects)
            self.save_m2m()

        return channel


class EpisodeForm(forms.ModelForm):
    class Meta:
        model = Episode
        fields = ['title', 'image', 'season', 'number', 'description',
                  'kind', 'episode', 'duration', 'explicit', 'guest',
                   ]#'created_on', 'updated_on']
        # widgets = {
        #     'episode': forms.ClearableFileInput(attrs={
        #
        #     })
        # }


    # def clean_guest(self):
    #     display_picture = self.cleaned_data['guest']
    #
    #     # print(display_picture)
    #     raise ValidationError('just checking stuffs')

    def save(self, request=None, channel=None, hx=False, commit=True):
        episode = super().save(commit=False)
        # print(channel)
        if channel:
            episode.channel = channel
            episode.status = 'Draft'
        if not hx:
            episode.save()
            self.save_m2m()

            return episode

        return episode

class FuturePublishForm(forms.ModelForm):



    class Meta:
        model = Episode
        fields = ['publish_date']
        widgets = {
            'publish_date': DateTimePickerInput(),
        }

    def save(self, commit=True):
        episode = super().save(commit=False)
        episode.status = 'Pending'
        episode.save()
        self.save_m2m()
        print('Publish_date=====> ', episode.publish_date)
        schedule, created = ClockedSchedule.objects.get_or_create(clocked_time=episode.publish_date)

        task = PeriodicTask.objects.update_or_create(clocked=schedule,
                                           name=f'publish_{episode.id}_at_{episode.publish_date.day}/{episode.publish_date.month}/{episode.publish_date.year}:{episode.publish_date.hour}:{episode.publish_date.minute}:{episode.publish_date.second}',
                                           task="podcasts.tasks.future_publish",
                                           args=json.dumps([str(episode.id),]),
                                           one_off=True)


        return episode

