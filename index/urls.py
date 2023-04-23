from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import index_page

urlpatterns = [
    path('', index_page, name='index')
]
