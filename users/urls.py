

from django.urls import path, include
from .views import ProfileDetail, ProfileUpdate, PublicProfileDetail

app_name = 'user'

urlpatterns = [

    path('<slug:username>/public', PublicProfileDetail.as_view(), name='public_profile'),
    path('<slug:username>/', ProfileDetail.as_view(), name='profile_detail'),
    path('<slug:username>/edit/', ProfileUpdate.as_view(), name='profile_update'),
]
