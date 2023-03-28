from django.urls import path
from .views import userLogin, userReg

urlpatterns = [
    path('login/', userLogin, name='login'),
    path('registration', userReg, name='reg')
]