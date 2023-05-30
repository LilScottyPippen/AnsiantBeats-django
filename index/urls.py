from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index_page, name='index'),
    path('beat/', beats_page, name='beats_page'),
    path('create_ticket', create_ticket, name='ticket')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
