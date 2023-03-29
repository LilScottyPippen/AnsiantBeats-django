from django.urls import path
from .views import userLogin, userReg, google_auth, google_callback

urlpatterns = [
    path('login/', userLogin, name='login'),
    path('registration', userReg, name='reg'),
    path('google/auth/', google_auth, name='google_auth'),
path('google/callback/', google_callback, name='google_callback')
]