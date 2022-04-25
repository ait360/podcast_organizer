from django.views.generic import DetailView, View
from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.urls import reverse_lazy



from .forms import UserUpdateForm, ProfileUpdateForm, UserCreateForm
from .models import Profile, User
from .utils import UpdateMixin, ProfileGetObjectMixin, ProfileGetUpdateObjectMixin

from allauth.account.views import SignupView

# Create your views here.



class SignUpView(SignupView):

    template_name = 'user/signup.html'
    form_class = UserCreateForm





    def get_success_url(self):
        user = get_user(self.request)

        if user.is_active and user.profile.name == '':
            return reverse_lazy('user_urls:profile_update', kwargs={'username':user.username})
        elif user.is_active and user.profile.name != '':
            return reverse_lazy('user_urls:profile_detail', kwargs={'username':user.username})

        return super().get_success_url()




class ProfileDetail(LoginRequiredMixin, ProfileGetObjectMixin,
                    DetailView):

    model = Profile
    slug_url_kwarg = 'slug'
    context_object_name = 'profile'
    template_name = 'user/profile_detail.html'


class PublicProfileDetail(DetailView):
    model = Profile

class ProfileUpdate(LoginRequiredMixin, UserPassesTestMixin,
                    ProfileGetObjectMixin, UpdateMixin, View):
    models = {'user': User, 'profile': Profile}
    form_classes = {'user_form': UserUpdateForm,
                    'profile_form': ProfileUpdateForm}
    template_name = 'user/profile_update.html'
    redirect_url_namespace = 'user_urls'

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user



