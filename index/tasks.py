from .models import Beat
from django.utils import timezone
from celery import shared_task


@shared_task
def update_beat_new_status():
    beats = Beat.objects.filter(isNew=True, created_at__lte=timezone.now() - timezone.timedelta(days=7))

    for beat in beats:
        beat.isNew = False
        beat.save()
