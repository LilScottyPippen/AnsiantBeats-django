from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Page
    path('', index_page, name='index'),
    path('beat/', beats_page, name='beats_page'),

    # Functions
    path('create_ticket', create_ticket_views, name='ticket'),
    path('filter', filter_beats, name='filter')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
