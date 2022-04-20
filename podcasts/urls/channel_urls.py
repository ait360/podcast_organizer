from django.urls import path, include
from ..views import (ChannelCreate, ChannelList,
                     ChannelDetail, ChannelUpdate,
                     ChannelDelete, ChannelSubcribe,
                     EpisodeCreate, #ChannelEpisodeList,
                     EpisodeUpdate, ChannelEpisodes,
                    )

app_name = 'podcasts'

urlpatterns = [
    path('', ChannelList.as_view(), name='channel_list'),
    path('create/', ChannelCreate.as_view(), name='channel_create'),
    path('<slug:slug>/', ChannelDetail.as_view(), name='channel_detail'),
    path('<slug:slug>/update/', ChannelUpdate.as_view(), name='channel_update'),
    path('<slug:slug>/delete/', ChannelDelete.as_view(), name='channel_delete'),
    path('<slug:slug>/subscribe/', ChannelSubcribe.as_view(), name='channel_subscribe'),
    path('<slug:slug>/episode-create/', EpisodeCreate.as_view(), name='episode_create'),
    # path('<slug:slug>/episodes/', ChannelEpisodeList.as_view(), name='channel_episodes'),
    path('<slug:slug>/episodes/', ChannelEpisodes.as_view(), name='channel_episodes'),
    path('<slug:slug>/<uuid:id>/update/', EpisodeUpdate.as_view(), name='episode_update'),





]