from django import forms
from django.contrib.auth import get_user_model
from django.utils.text import slugify
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Profile
from allauth.account.forms import SignupForm




class UserCreateForm(SignupForm): #, UserCreationForm):

    mail_validation_error = ('User created. Could not send activation '
                             'email. Please try again later. (Sorry!)')

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ('username', 'email')

    def clean_username(self):
        username = super().clean_username()
        #username = self.cleaned_data['username']
        disallowed = ('activate', 'signup', 'disable', 'login', 'logout',
                      'password', 'posts', 'tags', 'post', 'tag', 'ckeditor',
                      'admin')
        if username in disallowed:
            raise ValueError("A user with that username already exists.")
        # if username and get_user_model().objects.filter(username__iexact=username).exists():
        #     self.add_error('username', 'A user with that username already exists.')
        return username

    # def save(self, **kwargs):
    #     user = super().save(commit=False)
    #     if not user.pk:
    #         user.is_active = False
    #         user.is_member = True
    #         send_mail = True
    #     else:
    #         send_mail = False
    #     user.save()
    #     self.save_m2m()
    #     # Profile.objects.update_or_create(user=user,
    #     #                                       defaults={'slug': slugify(
    #     #                                           user.get_username()),})
    #     if send_mail:
    #         self.send_mail(user=user, **kwargs)


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('name', 'bio', 'website', 'phone_number',)


class UserUpdateForm(forms.ModelForm): #forms.ModelForm):

    class Meta:
        model = get_user_model()
        fields = ('display_picture', 'username', 'email',  'cover_picture')


    def clean_username(self):
        username = self.cleaned_data['username']
        disallowed = ('activate', 'signup', 'disable', 'login', 'logout',
                      'password')
        if username in disallowed:
            raise ValueError("A user with that username already exists.")
        return username

    def save(self, **kwargs):
        user = super().save(commit=False)
        if self.has_changed():

            if 'username' in self.changed_data:

                request = kwargs.get('request')
                profile = kwargs.get('profile')
                profile.slug=slugify(request.POST.get('username'))
                profile.save()
        user.save()
        return user