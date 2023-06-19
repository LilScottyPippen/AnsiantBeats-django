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

    if filter_type == 'key':
        beats = Beat.objects.filter(tonal__in=tonal_values)
    elif filter_type == 'mood':
        beats = Beat.objects.filter(mood__in=mood_values)
    elif filter_type == 'genres':
        try:
            beats = Beat.objects.filter(type__in=genre_values)
        except ValueError:
            beats = Beat.objects.all()
    elif filter_type == 'teg':
        if filter_value == 'new':
            beats = Beat.objects.filter(isNew=True)
        elif filter_value == 'gold':
            beats = Beat.objects.filter(isGold=True)
        elif filter_value == 'all':
            beats = Beat.objects.all()
        else:
            return JsonResponse({'message': 'Invalid filter value'}, status=400)
    elif filter_type == 'newest':
        if filter_value == 'ascending':
            beats = Beat.objects.order_by('price')
        elif filter_value == 'descending':
            beats = Beat.objects.order_by('-price')
        else:
            return JsonResponse({'message': 'Invalid filter value'}, status=400)
    elif filter_type == 'search':
        beats = Beat.objects.filter(title__icontains=filter_value)
    elif filter_type == 'price' and 'min_price' in filter_values and 'max_price' in filter_values:
        min_price = filter_values['min_price']
        max_price = filter_values['max_price']
        beats = Beat.objects.filter(price__gte=min_price, price__lte=max_price)
    elif 'min_bpm' in filter_values and 'max_bpm' in filter_values:
        min_bpm = filter_values['min_bpm']
        max_bpm = filter_values['max_bpm']
        beats = Beat.objects.filter(bpm__gte=min_bpm, bpm__lte=max_bpm)
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


@csrf_exempt
def apply_coupone(request):
    u_code = request.POST.get('code')
    print(u_code)
    sum = int(request.POST.get('sum'))
    print(sum)
    coupone = Coupone.objects.get(code=u_code)
    discount = int(coupone.discount)
    sum -= discount
    print(sum)
    return JsonResponse({'success': True, 'sum': sum, 'discount': discount}, safe=False)