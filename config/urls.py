"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .static import serve

from users.views import SignUpView
from allauth.account.views import LoginView






admin.site.site_header = 'Podcast Admin Platform'
admin.site.site_title = 'Podcast Admin Site'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('channel/', include('podcasts.urls.channel_urls', namespace='channel_urls')),
    path('', include('podcasts.urls.channel_urls')),
    path('user/', include('users.urls', namespace='user_urls')),
    path('episode/', include('podcasts.urls.episode_urls', namespace='episode_urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    #path('podcasts/', include('podcasts.urls', namespace='podcasts_urls')),
    path('accounts/', include('allauth.urls'),),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    #path("ckeditor5/", include('django_ckeditor_5.urls')),

]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, view=serve, document_root=settings.MEDIA_ROOT)
    # urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
