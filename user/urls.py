from django.urls import path
from .views import userLogin, userReg, google_auth, google_callback, reset_password, confirm_email, change_password

urlpatterns = [
    path('login/', userLogin, name='login'),
    path('registration', userReg, name='reg'),
    path('google/auth/', google_auth, name='google_auth'),
    path('google/callback/', google_callback, name='google_callback'),
    path('resetPassword/', reset_password, name='resetPassword'),
    path('resetPassword/<str:email>/<str:token>', confirm_email, name='confirmEmail'),
    path('changePassword/<str:email>/<str:token>', change_password, name='changePassword')
]