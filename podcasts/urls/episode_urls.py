from django.urls import path, include
from ..views import (EpisodeDetail, EpisodeDislike, EpisodeLike,
                     EpisodePublishNow, EpisodePublishLater, EpisodeListener,
                     DownloadEpisode)

app_name = 'podcasts'

urlpatterns = [
    # path('', ChannelList.as_view(), name='channel_list'),
    # path('create/', EpisodeCreate.as_view(), name='episode_create'),
    # path('<slug:slug>/', ChannelDetail.as_view(), name='channel_detail'),
    # path('<slug:slug>/update/', ChannelUpdate.as_view(), name='channel_update'),
    # path('<slug:slug>/delete/', ChannelDelete.as_view(), name='channel_delete'),
    # path('<slug:slug>/subscribe/', ChannelSubcribe.as_view(), name='channel_subscribe'),
    path('<uuid:id>/', EpisodeDetail.as_view(), name='episode_detail'),
    path('<uuid:id>/like', EpisodeLike.as_view(), name='episode_like'),
    path('<uuid:id>/dislike', EpisodeDislike.as_view(), name='episode_dislike'),
    path('<uuid:id>/publish', EpisodePublishNow.as_view(), name='episode_publish_now'),
    path('<uuid:id>/publish_later', EpisodePublishLater.as_view(), name='episode_publish_later'),
    path('<uuid:id>/paused', EpisodeListener.as_view(), name='episode_paused'),
    path('<uuid:id>/download', DownloadEpisode.as_view(), name='episode_download'),

]