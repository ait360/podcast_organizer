import json
from pathlib import Path
import mimetypes
from pprint import pprint
from http import HTTPStatus
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseForbidden, FileResponse, Http404
from django.contrib.auth import get_user
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.messages import success, error
from django.utils.translation import gettext_lazy as _
from django.forms.models import model_to_dict
from django.utils.text import slugify
from django.utils import timezone
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django_celery_beat.models import CrontabSchedule, PeriodicTask, ClockedSchedule


class HttpResponseNoContent(HttpResponse):
    status_code = HTTPStatus.NO_CONTENT


class ChannelCreateMixin:
    model = None
    form_class = None
    template_name = ''
    redirect_url_namesapce =''
    initial = {}
    context_object_name = None

    def get(self, request, *args, **kwargs):
        channel_form = self.form_class()
        context = {'form': channel_form}

        return render(request, self.template_name, context)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):

        if request.user.is_authenticated:



            channel_form = self.form_class(request.POST, request.FILES)

            if channel_form.is_valid():
                channel_form.save(request=request)
                success(request, _('Channel Created'))
                return redirect(self.get_success_url(request))
            else:
                context = {'form': channel_form}
                error(request, _("Please make corrections to the error(s) below"))
                return render(request, self.template_name, context)


    def get_success_url(self, request):
        username = request.POST['username']
        self.success_url = reverse_lazy(
            f'{self.redirect_url_namesapce}:{self.model.__name__.lower()}_detail',
            kwargs={'slug':slugify(username)}
        )
        return self.success_url


class ChannelUpdateMixin:
    model = None
    form_class = None
    template_name = ''
    redirect_url_namespace = ''
    initial  = {}
    context_object_name = None


    def get(self, request, slug, *args, **kwargs):
        channel = get_object_or_404(self.model, slug__iexact=slug)
        user = get_user(request)
        co_host = ', '.join(
            [host.username for host in channel.hosts.all() if not host == user])

        self.initial = model_to_dict(channel)
        self.initial['co_host']  = co_host


        channel_form = self.form_class(instance=channel, initial=self.initial)
        context = {
            'form': channel_form,
            self.context_object_name : channel
        }

        return render(request, self.template_name, context)

    @method_decorator(csrf_protect)
    def post(self, request, slug, *args, **kwargs):


        channel = get_object_or_404(self.model, slug__iexact=self.kwargs.get('slug'))

        hosts = channel.hosts.all()
        if request.user.is_authenticated and request.user in hosts:
            channel_form = self.form_class(request.POST, request.FILES,
                                           instance=channel, initial=self.initial)

            if channel_form.is_valid():
                channel_form.save(request)
                success(request, _("Channel Updated!!"))
                return redirect(self.get_success_url(request))
            else:
                context = {
                    'form': channel_form,
                    self.context_object_name: channel
                }
                error(request, _("Please make corrections to the error(s) below"))
                return render(request, self.template_name, context)

    def get_success_url(self, request):
        username = request.POST['username']
        self.success_url = reverse_lazy(
            f'{self.redirect_url_namesapce}:{self.model.__name__.lower()}_detail',
            kwargs={'slug': slugify(username)}
        )
        return self.success_url


class ChannelSubscribeMixin:
    model = None

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden("this Page is Forbidden")



    def post(self, request, *args, **kwargs):
        channel = self.model.objects.get(slug__iexact=self.kwargs.get('slug'))

        user = get_user(request)
        if user in channel.subscribers.all():
            channel.subscribers.remove(user)
        else:
            channel.subscribers.add(user, through_defaults={'subscribed': True})

        return render(request, "podcasts/partials/channel_subscribe.html",
                      {'channel': channel})




class EpisodeCreateMixin:
    model = None
    channel_model =None
    form_class = None
    template_name = ''
    redirect_url_namesapce =''
    initial = {}
    context_object_name = None

    def get(self, request, slug, *args, **kwargs):
        channel = get_object_or_404(self.channel_model, slug__iexact=slug)
        episode_form = self.form_class()
        context = {'form': episode_form,
                   'channel': channel}

        return render(request, self.template_name, context)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):


        channel = get_object_or_404(self.channel_model, slug__iexact=self.kwargs.get('slug'))

        hosts = channel.hosts.all()
        if request.user.is_authenticated and request.user in hosts:

            if request.htmx:
                if request.POST.get("episode_uuid", ''):
                    episode = self.model.objects.get(id__iexact=request.POST.get("episode_uuid"))

                    self.initial = model_to_dict(episode)
                    episode_form = self.form_class(request.POST, request.FILES,
                                                   instance=episode, initial=self.initial)

                else:
                    episode_form = self.form_class(request.POST, request.FILES)

                if episode_form.is_valid():
                    hx = False

                    ep = episode_form.save(request, channel, hx)

                    context = {'episode': ep}

                    return render(request, 'podcasts/partials/episode_create_partial.html', context)

                else:
                    context = {'form': episode_form}
                    error(request, _("Please make corrections to the error(s) below"))
                    return HttpResponseNoContent(_("Please make corrections to the error(s) below"))

            else:
                episode = self.model.objects.get(id__iexact=request.POST.get('episode_uuid'))

                self.initial = model_to_dict(episode)
                # episode_file = request.FILES.pop('episode')
                episode_form = self.form_class(request.POST, request.FILES,
                                            instance=episode, initial=self.initial)
                if episode_form.is_valid():
                    episode_form.save()

                    success(request, _('Episode Created'))
                    return redirect(self.get_success_url(request))
                else:
                    context = {'form': episode_form}
                    error(request, _("Please make corrections to the error(s) below"))
                    return render(request, self.template_name, context)


    def get_success_url(self, request):
        return reverse_lazy('channel_urls:channel_episodes', kwargs={'slug':self.kwargs.get('slug')})


class EpisodeUpdateMixin:
    model = None
    channel_model = None
    form_class = None
    template_name = ''
    redirect_url_namespace = ''
    initial  = {}
    context_object_name = ''


    def get(self, request, *args, **kwargs):
        channel = get_object_or_404(self.channel_model, slug__iexact=kwargs.get('slug'))
        episode = self.get_object()
        user = get_user(request)
        # co_host = ', '.join(
        #     [host.username for host in channel.hosts.all() if not host == user])

        self.initial = model_to_dict(episode)
        # self.initial['co_host']  = co_host


        episode_form = self.form_class(instance=episode, initial=self.initial)
        context = {
            'form': episode_form,
            self.context_object_name : episode
        }

        return render(request, self.template_name, context)

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        channel = get_object_or_404(self.channel_model, slug__iexact=kwargs.get('slug'))


        hosts = channel.hosts.all()
        if request.user.is_authenticated and request.user in hosts:
            if request.htmx:

                episode = self.get_object()

                self.initial = model_to_dict(episode)
                episode_form = self.form_class(request.POST or None, request.FILES or None,
                                               instance=episode, initial=self.initial)


                if episode_form.is_valid():
                    hx = False

                    ep = episode_form.save(request, channel, hx)

                    context = {'episode': ep}

                    return render(request, 'podcasts/partials/episode_create_partial.html', context)

                else:
                    context = {'form': episode_form}
                    error(request, _("Please make corrections to the error(s) below"))
                    return HttpResponseNoContent(_("Please make corrections to the error(s) below"))

            else:
                episode = self.get_object()

                self.initial = model_to_dict(episode)
                # episode_file = request.FILES.pop('episode')
                episode_form = self.form_class(request.POST or None, request.FILES or None,
                                            instance=episode, initial=self.initial)
                if episode_form.is_valid():
                    episode_form.save()

                    success(request, _('Episode Updated'))
                    return redirect(self.get_success_url(request))
                else:
                    context = {'form': episode_form}
                    error(request, _("Please make corrections to the error(s) below"))
                    return render(request, self.template_name, context)



    def get_success_url(self, request):
        # username = request.POST['username']
        # self.success_url = reverse_lazy(
        #     f'{self.redirect_url_namesapce}:{self.model.__name__.lower()}_detail',
        #     kwargs={'slug': slugify(username)}
        # )
        print(self.kwargs)
        return reverse_lazy('channel_urls:channel_episodes', kwargs={
                                                            'slug': self.kwargs.get('slug')})

    def get_object(self):
        episode = get_object_or_404(self.model, id__iexact=str(self.kwargs.get('id')))
        return episode


class EpisodeLikeMixin:
    model = None

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden("this Page is Forbidden")

    def post(self, request, *args, **kwargs):
        episode = self.model.objects.get(id__iexact=str(self.kwargs.get('id')))

        user = get_user(request)
        if user in episode.likes.all():
            episode.likes.remove(user)
        else:
            if user in episode.dislikes.all():
                episode.dislikes.remove(user)
            episode.likes.add(user, through_defaults={'liked': True})

        return render(request, "podcasts/partials/episode_like_dislike.html",
                      {'episode': episode})

class EpisodeDislikeMixin:
    model = None

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden("<p>this Page is Forbidden</p>")

    def post(self, request, *args, **kwargs):
        episode = self.model.objects.get(id__iexact=str(self.kwargs.get('id')))

        user = get_user(request)
        if user in episode.dislikes.all():
            episode.dislikes.remove(user)
        else:
            if user in episode.likes.all():

                episode.likes.remove(user)

            episode.dislikes.add(user, through_defaults={'disliked': True})

        return render(request, "podcasts/partials/episode_like_dislike.html",
                      {'episode': episode})


class EpisodePublishNowMixin:
    model  = None

    def post(self, request, *args, **kwargs):
        episode = get_object_or_404(self.model, id__iexact=str(self.kwargs.get('id')))
        # episode = self.model.objects.get(id__iexact=str(self.kwargs.get('id')))

        if episode.publish_date:
            episode.status = 'Withdrawn'
            episode.publish_date = None
            try:
                task = PeriodicTask.objects.get(name=f'publish_{episode.id}_at_{episode.publish_date.day}/{episode.publish_date.month}/{episode.publish_date.year}:{episode.publish_date.hour}:{episode.publish_date.minute}:{episode.publish_date.second}')
                print(task)
                task.delete()
            except:
                print('ignored')

        else:
            episode.publish_date = timezone.now()
            episode.status = 'Published'
        episode.save()

        return render(request, "podcasts/partials/episode_status.html",
                      {'episode': episode})


class EpisodePublishLaterMixin:
    model = None
    form_class = None

    def get(self, request, *args, **kwargs):
        episode = get_object_or_404(self.model, id__iexact=str(self.kwargs.get('id')))
        self.initial = model_to_dict(episode)
        episode_form = self.form_class(instance=episode, initial=self.initial)
        context = {
            'episode': episode,
            'form': episode_form,
        }
        return render(request,
                      "podcasts/partials/episode_publish_later.html",
                      context)

    def post(self, request, *args, **kwargs):
        episode = get_object_or_404(self.model, id__iexact=str(self.kwargs.get('id')))

        episode_form = self.form_class(request.POST or None,
                                               instance=episode)

        if episode_form.is_valid():
            episode = episode_form.save()



            pub_date = episode.publish_date
            success(request, _(f'Episode will be available on {pub_date.day}/{pub_date.month}'
            f'/{pub_date.year} at {pub_date.hour}:{pub_date.minute}'))
            return render(request, "podcasts/partials/episode_status.html",
                          {'episode': episode})
        else:
            context = {'form': episode_form,
                       'episode': episode}
            error(request, _("Please make corrections to the error(s) below"))
            return render(request,
                          "podcasts/partials/episode_publish_later.html",
                          context)

class EpisodeListenerMixin:
    model = None

    def get(self, request, *args, **kwargs):
        return HttpResponseForbidden("<p>this Page is Forbidden</p>")

    def post(self, request, *args, **kwargs):
        episode = self.model.objects.get(id__iexact=str(self.kwargs.get('id')))

        print(request.POST)
        user = get_user(request)
        print(user)
        pprint(request.META)
        print(type(request.META))
        self.time_listened = float(request.META.get('HTTP_CURRENT', 0))
        self.start_time = float(request.META.get('HTTP_START', 0))
        self.start = request.META.get('HTTP_PLAYING', 'no')
        print('self.start', self.start)
        print(self.time_listened)
        print('start time', self.start_time)
        print('start again', self.start)
        self.time_streamed_percent = 0.3 * episode.duration
        self.time_listened_percent = 0.95 * episode.duration
        self.start_time_percent = 0.05 * episode.duration
        print(self.time_listened_percent)
        print(episode.duration)

        if user in episode.listeners.all():
            print('I CAME HERE IS ALL CAPS')
            listener = episode.listeners.through.objects.get(user=user, episode=episode)
            if self.start == 'yes':
                'this will be from a play button'
                listener.start_time = self.start_time
                listener.save()
                print('start time after save ', listener.start_time)
                return HttpResponse('Playing')

            else:
                #this will be from a pause button"
                self.start_time = listener.start_time
                listener.time_listened = self.time_listened
                if self.start_time < self.start_time_percent and self.time_listened >= self.time_streamed_percent:
                    listener.streams += 1
                if self.start_time < self.start_time_percent and self.time_listened >= self.time_listened_percent:
                    listener.streams += 1
                    listener.completed_count += 1
                    if not listener.listened:
                        listener.listened = True
                listener.save()
                print('start time after save pause ', listener.start_time)
                print('current time after save pause', listener.time_listened)
                return HttpResponse('Paused')

        else:
            print('I CAME HERE IS ALL CAPS 2!!!')
            episode.listeners.add(user, through_defaults={'start_time': self.start_time})


            return HttpResponse('Playing')




class DownloadEpisodeMixin:

    model  = None

    def get(self, request, *args, **kwargs):
        episode = self.model.objects.get(id__iexact=str(self.kwargs.get('id')))

        path = episode.episode.path
        fullpath = Path(path)
        if fullpath.is_dir():
            raise Http404(_("Direcotry indexes are not allowed here."))

        if not fullpath.exists():
            raise Http404(_('“%(path)s” does not exist') % {'path': fullpath})

        statobj = fullpath.stat()

        content_type, encoding = mimetypes.guess_type(str(fullpath))
        content_type = content_type or 'application/octet-stream'
        response = FileResponse(fullpath.open('rb'), as_attachment=True)
        response.headers['Content-Length'] = statobj.st_size
        response.headers['Accept-Ranges'] = 'bytes'
        response.headers['Content-Type'] = content_type
        if encoding:
            response.headers['Content-Encoding'] = encoding

        return response