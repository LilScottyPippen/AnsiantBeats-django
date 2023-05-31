from django.urls import path
from .views import *

urlpatterns = [
    # Page
    path('authorization/', user_login, name='auth'),
    path('login/', authorization_page, name='login'),
    path('registration/', registration_page, name='reg'),
    path('shopping-cart/', shopping_cart, name='shop_cart'),
    path('profile/', user_profile_page, name='profile'),

    # Functions
    path('logout/', user_logout, name='logout'),
    path('google/auth/', google_auth, name='google_auth'),
    path('google/callback/', google_callback, name='google_callback'),
    path('add_to_cart/', add_to_cart, name='add_to_cart'),
    path('get_cart', get_cart, name='get_cart'),
    path('get_license', get_license, name='get_license'),
    path('delete_item/', delete_item, name='delete_item'),
    path('create_order/', create_order, name='create_order'),
    path('confirm_code/', registration_code, name='code'),
    path('registration_user/', reg, name='registration'),

    # Make AJAX
    path('resetPassword/', reset_password, name='resetPassword'),
    path('resetPassword/<str:email>/<str:token>', confirm_email, name='confirmEmail'),
    path('changePassword/<str:email>/<str:token>', change_password, name='changePassword'),
]