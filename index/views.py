from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Beat, Tonal, Types, Mood
from django.db.models import Min, Max
from .tasks import create_ticket


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
    elif filter_type == 'reset':
        beats = Beat.objects.all()
    else:
        return JsonResponse({'message': 'Invalid filter type'}, status=400)

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
def create_ticket_views(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    description = request.POST.get("description")

    create_ticket.delay(name, email, subject, description)

    return JsonResponse({'success': True}, safe=False)