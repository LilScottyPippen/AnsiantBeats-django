from django.urls import path
from .views import index_page, create_ticket
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index_page, name='index'),
    path('create_ticket', create_ticket, name='ticket')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
