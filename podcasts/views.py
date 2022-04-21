from pprint import pprint
from django.shortcuts import render, redirect
from django.views.generic import (CreateView, UpdateView, DetailView,
                                  ListView, DeleteView)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import View
from django.contrib.auth import get_user
from .models import Channel, Episode, Like, Subscriber
from .forms import ChannelForm, EpisodeForm, FuturePublishForm
from .utils import ChannelCreateMixin, ChannelUpdateMixin, ChannelSubscribeMixin, \
    EpisodeCreateMixin, EpisodeLikeMixin, EpisodeUpdateMixin, EpisodeDislikeMixin, \
    EpisodePublishNowMixin, EpisodePublishLaterMixin, EpisodeListenerMixin, \
    DownloadEpisodeMixin
from django.urls import reverse_lazy
from django.http.response import HttpResponse
from django.core import serializers
from django.shortcuts import get_object_or_404

# Create your views here.






class ChannelCreate(LoginRequiredMixin, ChannelCreateMixin, View):
    model = Channel
    form_class = ChannelForm
    template_name = 'podcasts/channel_create.html'
    redirect_url_namesapce = 'channel_urls'
    context_object_name = 'channel'

class ChannelDetail(DetailView):
    model = Channel
    context_object_name = 'channel'
    slug_url_kwarg = 'slug'
    template_name = 'podcasts/channel_detail.html'

class ChannelUpdate(LoginRequiredMixin, UserPassesTestMixin,
                    ChannelUpdateMixin, UpdateView):
    model = Channel
    form_class = ChannelForm
    template_name = 'podcasts/channel_update.html'
    redirect_url_namesapce = 'channel_urls'
    context_object_name = 'channel'

    def test_func(self):
        channel = self.get_object()
        return self.request.user in channel.hosts.all()

class ChannelDelete(LoginRequiredMixin, UserPassesTestMixin,
                    DeleteView):
    model = Channel
    success_url = reverse_lazy('channel_urls:channel_list')
    context_object_name = 'channel'
    template_name = 'podcasts/channel_confirm_delete.html'

    def test_func(self):
        channel = self.get_object()
        return self.request.user in channel.hosts.all()

class ChannelList(LoginRequiredMixin, ListView):
    model = Channel
    context_object_name = 'channel_list'
    template_name = 'podcasts/channel_list.html'

    def get(self, request, *args, **kwargs):
        user = get_user(request)
        if not user.profile.name:
            return redirect(user.profile.get_update_url())

        else:
            return super(ChannelList, self).get(request, *args, **kwargs)

    #Remember to list channels according to channels subscribed to
    # via the get_queryset method and do something like this
    # def get_queryset(self):
    #     user = self.request.user
    #     return user.subscribers.all()



class ChannelSubcribe(LoginRequiredMixin, ChannelSubscribeMixin, View):
    model = Channel


class ChannelEpisodes(LoginRequiredMixin, ListView):
    model = Episode
    context_object_name = 'channel_episodes'
    template_name = 'podcasts/channel_episode_list.html'
    paginate_by = 5

    def get_template_names(self):
        if self.request.htmx:
            return 'podcasts/partials/channel_episode_partial.html'
        return self.template_name

    def get_queryset(self):
        # pprint(self.request.META)

        user = get_user(self.request)
        channel = Channel.objects.get(slug=self.kwargs.get('slug'))

        if user in channel.hosts.all():
            self.episodes = self.model.objects.filter(channel=channel).order_by('publish_date', 'created_on')#get_object_or_404(self.model, slug__iexact=self.kwargs.get('slug'))
            return self.episodes

        else:
            self.episodes = self.model.objects.filter(channel=channel, status='Published').order_by('publish_date', 'created_on')
            return self.episodes


    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['channel'] = Channel.objects.get(slug=self.kwargs.get('slug'))
        context['channelepisodes'] = [episode.episode.url for episode in self.get_queryset()]

        return context


class EpisodeCreate(LoginRequiredMixin, UserPassesTestMixin,
                    EpisodeCreateMixin, View):
    model = Episode
    channel_model = Channel
    form_class = EpisodeForm
    template_name = 'podcasts/episode_create.html'
    redirect_url_namesapce = 'channel_urls'
    context_object_name = 'episode'

    def test_func(self):
        channel = get_object_or_404(self.channel_model, slug__iexact=self.kwargs.get('slug'))
        return self.request.user in channel.hosts.all()

class EpisodeUpdate(LoginRequiredMixin, UserPassesTestMixin,
                    EpisodeUpdateMixin, View):
    model = Episode
    channel_model = Channel
    form_class = EpisodeForm
    template_name = 'podcasts/episode_update.html'
    redirect_url_namespace = 'channel_urls'
    context_object_name = 'episode'

    def test_func(self):
        episode = self.get_object()
        return self.request.user in episode.channel.hosts.all()

class EpisodeDetail(DetailView):
    model = Episode
    slug_field = 'id'
    slug_url_kwarg = 'id'
    template_name = 'podcasts/episode_detail.html'
    context_object_name = 'episode'


class EpisodeLike(LoginRequiredMixin, EpisodeLikeMixin, View):
    model = Episode

class EpisodeDislike(LoginRequiredMixin, EpisodeDislikeMixin, View):
    model = Episode

class EpisodePublishNow(LoginRequiredMixin, EpisodePublishNowMixin, View):
    model = Episode



class EpisodePublishLater(LoginRequiredMixin, EpisodePublishLaterMixin, View):
    model = Episode
    form_class = FuturePublishForm

class EpisodeListener(LoginRequiredMixin, EpisodeListenerMixin, View):
    model = Episode

class DownloadEpisode(LoginRequiredMixin, DownloadEpisodeMixin, View):
    model = Episode