from django import template
from ..models import Listener

register = template.Library()



@register.simple_tag
def listener(user, episode):

    try:
        listener_obj = Listener.objects.get(user=user, episode=episode)
    except Listener.DoesNotExist:
        return False
    return listener_obj