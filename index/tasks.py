from django.utils import timezone
from celery import shared_task
from django.conf import settings
from .models import Beat, Ticket
from user.models import CustomUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from AB.celery import app


@shared_task
def update_beat_new_status():
    beats = Beat.objects.filter(isNew=True, created_at__lte=timezone.now() - timezone.timedelta(days=7))

    for beat in beats:
        beat.isNew = False
        beat.save()


@app.task
def create_ticket(name, email, subject, description):
    ticket = Ticket.objects.create(name=name, email=email, subject=subject, description=description)

    # User
    message = render_to_string('index/notification.html', {'name': name, 'subject': subject,
                                                           'description': description, 'ticket_id': ticket.id})
    recipient_list = [email]
    send_mail(subject, message, settings.EMAIL_HOST, recipient_list, fail_silently=False)

    # Admin
    message = render_to_string('index/admin_notification.html', {'name': name, 'email': email, 'subject': subject,
                                                                 'description': description, 'ticket_id': ticket.id})
    recipient_list = [admin.email for admin in CustomUser.objects.filter(is_superuser=True)]
    send_mail(subject, message, settings.EMAIL_HOST, recipient_list, fail_silently=False)

