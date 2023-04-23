from django.shortcuts import render
from .models import Beat


def index_page(request):
    beat = Beat.objects.order_by('beat_id')
    last_beat = Beat.objects.order_by('-beat_id')[:3]

    context = {
        'beat': beat,
        'last_beat': last_beat,
    }
    return render(request, 'index/main.html', context)
