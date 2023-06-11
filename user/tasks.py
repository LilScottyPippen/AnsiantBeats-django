from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from AB.celery import app


@app.task()
def send_verification_email(email, code):
    subject = 'Email verification code'
    message = render_to_string('user/verification_email.html', {'code': code})
    recipient_list = [email]
    send_mail(subject, message, settings.EMAIL_HOST, recipient_list, fail_silently=False)