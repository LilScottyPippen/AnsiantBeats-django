from django.shortcuts import render
from .models import Beat


def index_page(request):
    beat = Beat.objects.order_by('beat_id')
    last_beat = Beat.objects.order_by('-beat_id')[:3]

    cart = request.session.get('cart', {})

    amount = 0
    for item in cart.values():
        beat_cart = Beat.objects.get(beat_id=item['id'])
        amount += beat_cart.price
    context = {
        'beat': beat,
        'last_beat': last_beat,
        'amount': amount,
        'cart': cart
    }
    return render(request, 'index/main.html', context)