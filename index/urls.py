from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Page
    path('', index_page, name='index'),
    path('beat/', beats_page, name='beats_page'),
    path('policy', policy_page, name='policy'),
    path('license', license_page, name='license'),

    # Functions
    path('create_ticket', create_ticket_views, name='ticket'),
    path('filter', filter_beats, name='filter'),
    path('coupon', apply_coupon, name='coupon')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
