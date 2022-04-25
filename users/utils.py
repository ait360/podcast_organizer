import logging
from logging import CRITICAL, ERROR
import traceback
from smtplib import SMTPException
from django.contrib.auth.tokens import default_token_generator as \
    token_generator
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.contrib.auth import get_user
from django.contrib.messages import success, error
from django.contrib.sites.shortcuts import get_current_site
from django.core.exceptions import ValidationError
from django.db.models.fields.related import ManyToManyField
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404, render, redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.decorators.csrf import csrf_protect
from django.utils.text import slugify
from .models import Profile
from django.views.generic import UpdateView as BaseUpdateView

class UpdateMixin:
    models = {}
    form_classes = {}
    template_name = ''
    redirect_url_namespace=''
    initial = {}

    def get(self, request, username):
        user = get_object_or_404(self.models['user'], profile__slug__iexact=slugify(username))
        self.initial = model_to_dict(user)
        profile = get_object_or_404(self.models['profile'],
                                    slug__iexact=slugify(username))


        user_form = self.form_classes['user_form'](instance=user, initial=self.initial)
        profile_form = self.form_classes['profile_form'](instance=profile)
        context= {'user_form': user_form, 'profile_form': profile_form,
                  'user' : user, self.models['profile'].__name__.lower():profile}

        return render(request, self.template_name, context)


    @method_decorator(csrf_protect)
    def post(self, request, username):
        user = get_object_or_404(self.models['user'], profile__slug__iexact=slugify(username))
        profile = get_object_or_404(self.models['profile'],
                                    slug__iexact=slugify(username))

        if request.user.is_authenticated and request.user.id == user.id:
            user_form = self.form_classes['user_form'](request.POST, request.FILES,
                                                  instance=request.user,
                                                  initial=self.initial)
            profile_form = self.form_classes['profile_form'](request.POST,
                                request.FILES, instance=profile)

            if user_form.is_valid() and profile_form.is_valid():
                user = user_form.save(request=request, profile=profile)
                profile_form.save()
                success(request, _('Updated!!'))
                return redirect(self.get_success_url(username=user.username))
            else:
                context = {'user_form': user_form, 'profile_form': profile_form,
                  'user' : user, self.models['profile'].__name__.lower():profile}
                error(request, _('Please correct the error(s) below'))
                return render(request, self.template_name, context)

    def get_success_url(self, username):
        self.success_url = reverse_lazy('{}:{}_detail'.format(
            self.redirect_url_namespace,
            self.models['profile'].__name__.lower()), kwargs={'username':slugify(username)})
        return self.success_url

class ProfileGetObjectMixin:

    def get_object(self, queryset=None):

        try:
            profile = get_object_or_404(self.models['profile'], slug__iexact=slugify(self.kwargs.get('username')))
            return profile
        except:
            profile = get_object_or_404(self.model, slug__iexact=slugify(self.kwargs.get('username')))
            return profile


class ProfileGetUpdateObjectMixin:

    def get_object(self, queryset=None):
        profile = get_object_or_404(self.models['profile'], slug__iexact=slugify(self.kwargs.get('username')))
        return profile



