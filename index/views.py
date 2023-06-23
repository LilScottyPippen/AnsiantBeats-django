from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Beat, Tonal, Types, Mood, Coupone
from django.db.models import Min, Max
from .tasks import create_ticket


def index_page(request):
    last_beat = Beat.objects.order_by('-beat_id')[:3]

    cart = request.session.get('cart', {})

    amount = 0
    for item in cart.values():
        beat_cart = Beat.objects.get(beat_id=item['id'])
        amount += beat_cart.price
    request.session['amount'] = amount
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

    if request.session.get('filter_values'):
        del request.session['filter_values']

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

    filter_values = request.session.get('filter_values', {})

    if filter_type == 'key':
        tonal_values = filter_values.get('tonal', [])
        if filter_value in tonal_values:
            tonal_values.remove(filter_value)
        else:
            tonal_values.append(filter_value)
        filter_values['tonal'] = tonal_values
    elif filter_type == 'mood':
        mood_values = filter_values.get('mood', [])
        if filter_value in mood_values:
            mood_values.remove(filter_value)
        else:
            mood_values.append(filter_value)
        filter_values['mood'] = mood_values
    elif filter_type == 'genres':
        genre_values = filter_values.get('genres', [])
        if filter_value in genre_values:
            genre_values.remove(filter_value)
        else:
            genre_values.append(filter_value)
        filter_values['genres'] = genre_values
    elif filter_type == 'teg':
        teg_values = filter_values.get('teg', [])
        if filter_value in teg_values:
            teg_values.remove(filter_value)
        else:
            teg_values.append(filter_value)
        filter_values['teg'] = teg_values
    elif filter_type == 'newest':
        if filter_value == 'ascending':
            filter_values['newest'] = 'ascending'
        elif filter_value == 'descending':
            filter_values['newest'] = 'descending'
    elif filter_type == 'price':
        filter_values['min_price'] = request.POST.get('min')
        filter_values['max_price'] = request.POST.get('max')
    elif filter_type == 'bpm':
        filter_values['min_bpm'] = request.POST.get('min')
        filter_values['max_bpm'] = request.POST.get('max')
    elif filter_type == 'search':
        filter_values['search'] = filter_value
    elif filter_type == 'reset':
        filter_values = {}
    else:
        return JsonResponse({'message': 'Invalid filter type'}, status=400)

    request.session['filter_values'] = filter_values

    print(filter_values)

    beats = Beat.objects.all()

    if 'newest' in filter_values:
        newest_value = filter_values['newest']
        if newest_value == 'ascending':
            beats = beats.order_by('price')
        elif newest_value == 'descending':
            beats = beats.order_by('-price')

    if 'tonal' in filter_values:
        tonal_values = filter_values['tonal']
        beats = beats.filter(tonal__in=tonal_values)

    if 'mood' in filter_values:
        mood_values = filter_values['mood']
        beats = beats.filter(mood__in=mood_values)

    if 'genres' in filter_values:
        genre_values = filter_values['genres']
        beats = beats.filter(type__in=genre_values)

    if 'teg' in filter_type:
        if 'new' in filter_value:
            beats = beats.filter(isNew=True)
        elif 'gold' in filter_value:
            beats = beats.filter(isGold=True)

    if filter_type == 'search' and 'search' in filter_values:
        search_value = filter_values['search']
        beats = beats.filter(title__icontains=search_value)

    if filter_type == 'price' and 'min_price' in filter_values and 'max_price' in filter_values:
        min_price = filter_values['min_price']
        max_price = filter_values['max_price']
        beats = beats.filter(price__gte=min_price, price__lte=max_price)

    if 'min_bpm' in filter_values and 'max_bpm' in filter_values:
        min_bpm = filter_values['min_bpm']
        max_bpm = filter_values['max_bpm']
        beats = beats.filter(bpm__gte=min_bpm, bpm__lte=max_bpm)
        print(beats)

    if filter_type == 'reset':
        beats = Beat.objects.all()

    cart_keys = list(request.session.get('cart', {}).keys())
    beat_data = [
        {
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
        }
        for beat in beats
    ]
    return JsonResponse({'beats': beat_data}, safe=False)


@csrf_exempt
def create_ticket_views(request):
    name = request.POST.get("name")
    email = request.POST.get("email")
    subject = request.POST.get("subject")
    description = request.POST.get("description")

    create_ticket.delay(name, email, subject, description)

    return JsonResponse({'success': True}, safe=False)


@csrf_exempt
def apply_coupon(request):
    u_code = request.POST.get('code')
    sum = int(request.POST.get('sum'))
    coupon = Coupone.objects.get(code=u_code)
    discount = int(coupon.discount)
    sum -= discount
    return JsonResponse({'success': True, 'sum': sum, 'discount': discount}, safe=False)


def policy_page(request):
    amount = request.session.get('amount')
    context = {
        'amount': amount
    }
    return render(request, 'index/policy.html', context)


def license_page(request):
    amount = request.session.get('amount')
    context = {
        'amount': amount
    }
    return render(request, 'index/license.html', context)
