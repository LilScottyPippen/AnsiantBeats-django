from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Beat, Ticket
from user.models import CustomUser
from django.core.mail import send_mail
from django.template.loader import render_to_string



def index_page(request):
    last_beat = Beat.objects.order_by('-beat_id')[:3]

    cart = request.session.get('cart', {})

    amount = 0
    for item in cart.values():
        beat_cart = Beat.objects.get(beat_id=item['id'])
        amount += beat_cart.price
    context = {
        'last_beat': last_beat,
        'amount': amount,
        'cart': cart
    }
    return render(request, 'index/home.html', context)


def beats_page(request):
    beat = Beat.objects.order_by('beat_id')

    cart = request.session.get('cart', {})

    amount = 0
    for item in cart.values():
        beat_cart = Beat.objects.get(beat_id=item['id'])
        amount += beat_cart.price

    context = {
        'beat': beat,
        'amount': amount,
        'cart': cart
    }
    return render(request, 'index/playlist.html', context)


@csrf_exempt
def create_ticket(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    description = request.POST.get("description")
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

    return JsonResponse({'success': True}, safe=False)