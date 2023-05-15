from django.urls import path
from .views import user_login, user_reg, user_logout, google_auth, google_callback, \
    reset_password, confirm_email, change_password, user_profile, shopping_cart, \
    add_to_cart, get_cart, delete_item, create_order, get_license

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
    path('shopping-cart/', shopping_cart, name='shop_cart'),
    path('add_to_cart/<int:beat_id>', add_to_cart, name='add_to_cart'),
    path('get_cart', get_cart, name='get_cart'),
    path('get_license', get_license, name='get_license'),
    path('delete_item/<int:pk>', delete_item, name='delete_item'),
    path('create_order/', create_order, name='create_order')
]