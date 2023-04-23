from django.urls import path
from .views import user_login, user_reg, user_logout, google_auth, google_callback, \
    reset_password, confirm_email, change_password, user_profile, shopping_cart

urlpatterns = [
    path('login/', user_login, name='login'),
    path('registration/', user_reg, name='reg'),
    path('logout/', user_logout, name='logout'),
    path('google/auth/', google_auth, name='google_auth'),
    path('google/callback/', google_callback, name='google_callback'),
    path('resetPassword/', reset_password, name='resetPassword'),
    path('resetPassword/<str:email>/<str:token>', confirm_email, name='confirmEmail'),
    path('changePassword/<str:email>/<str:token>', change_password, name='changePassword'),
    path('profile/', user_profile, name='profile'),
    path('shopping-cart/', shopping_cart, name='shop_cart')
]