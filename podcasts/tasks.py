import json
from celery import shared_task
from .models import Episode


@shared_task(bind=True)
def future_publish(self, id):
    print(f'{id} got here')
    episode = Episode.objects.get(id=id)
    episode.status = 'Published'
    episode.save()
    return 'Done'
