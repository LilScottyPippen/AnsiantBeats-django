from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .models import Beat, Ticket, Tonal, Types, Mood
from user.models import CustomUser
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.db.models import Min, Max


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
    keys = Tonal.objects.all()
    mood = Mood.objects.all()
    genres = Types.objects.all()
    min_price = Beat.objects.aggregate(min_price=Min('price'))['min_price']
    max_price = Beat.objects.aggregate(max_price=Max('price'))['max_price']
    min_bpm = Beat.objects.aggregate(min_bpm=Min('bpm'))['min_bpm']
    max_bpm = Beat.objects.aggregate(max_bpm=Max('bpm'))['max_bpm']

    cart = request.session.get('cart', {})

    amount = 0
    for item in cart.values():
        beat_cart = Beat.objects.get(beat_id=item['id'])
        amount += beat_cart.price

    context = {
        'beat': beat,
        'key': keys,
        'mood': mood,
        'genre': genres,
        'min_price': min_price,
        'max_price': max_price,
        'min_bpm': min_bpm,
        'max_bpm': max_bpm,
        'amount': amount,
        'cart': cart
    }
    return render(request, 'index/playlist.html', context)


@csrf_exempt
def filter_beats(request):
    filter_type = request.POST.get('filterType')
    filter_value = request.POST.get('filterValue')

    if filter_type == 'key':
        beats = Beat.objects.filter(tonal=filter_value)
    elif filter_type == 'mood':
        beats = Beat.objects.filter(mood=filter_value)
    elif filter_type == 'newest':
        if filter_value == 'ascending':
            beats = Beat.objects.order_by('price')
        elif filter_value == 'descending':
            beats = Beat.objects.order_by('-price')
    elif filter_type == 'search':
        beats = Beat.objects.filter(title__icontains=filter_value)
    else:
        return JsonResponse({'error': 'Invalid filter type'}, status=400)

    cart_keys = list(request.session.get('cart', {}).keys())
    beat_data = list(map(lambda beat: {
        'beat_id': beat.beat_id,
        'title': beat.title,
        'cover': beat.cover,
        'beat': beat.beat,
        'type': beat.type.title,
        'tonal': beat.tonal.title,
        'isNew': beat.isNew,
        'isGold': beat.isGold,
        'isAddedToCart': str(beat.beat_id) in cart_keys,
        'duration': beat.duration,
        'bpm': beat.bpm,
        'price': beat.price,
    }, beats))
    return JsonResponse({'beats': beat_data}, safe=False)


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