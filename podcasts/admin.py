from django.contrib import admin
from .models import Channel, Episode, Like, Subscriber, Listener
from django.utils.text import slugify

# Register your models here.

admin.site.register(Episode)
admin.site.register(Like)
admin.site.register(Subscriber)
admin.site.register(Listener)


@admin.register(Channel)
class ChannelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        obj.slug = slugify(obj.username)
        super().save_model(request, obj, form, change)