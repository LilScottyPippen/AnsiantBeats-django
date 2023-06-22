import json
import uuid
import random
import requests
import urllib.parse
from index.models import Beat
from django.urls import reverse
from django.conf import settings
from django.db.models import Max
from django.core import serializers
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from .tasks import send_verification_email
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse
from .models import CustomUser, GoogleCredentials, Order, OrderItems, License

User = get_user_model()

ERROR_MESSAGES = {
    'invalid_request': 'Invalid request!',
    'invalid_credentials': 'Invalid email or password!',
    'email_registered': 'This email is already registered!',
    'email_send_error': 'Error sending email!',
    'invalid_code': 'Invalid code!',
    'max_level': "It's maximum license level!",
    'order_not_exist': 'Order item does not exist!',
    'license_not_exist': 'License does not exist!',
    'invalid_pass': 'Invalid password!'
}

SUCCESS_MESSAGES = {
    'auth': 'You have successfully logged in!',
    'reg': 'You have successfully registered!',
    'code_confirm': 'Code send to email!',
    'improve_license': 'License improve!',
    'order_created': 'Order created!',
    'changed_pass': 'The password has been successfully changed!'
}


def authorization_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'user/autorization.html')


def registration_page(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'user/registr.html')


@login_required(login_url='login')
def user_profile_page(request):
    try:
        order = Order.objects.filter(user_id=request.user)
        beat = OrderItems.objects.filter(order_id__in=order)
    except Exception as e:
        return JsonResponse({'success': True, 'message': str(e)})
    context = {
        'beat': beat,
    }
    return render(request, 'user/cab.html', context)


@csrf_exempt
def reset_password(request):
    try:
        if request.method == 'POST':
            current_password = request.POST.get('old_pass')
            if request.user.check_password(current_password):
                email = request.user.email
                code = ''
                for i in range(6):
                    code += str(random.randint(0, 9))
                cache.set(email, code, 300)
                send_verification_email.delay(email, code, 'reset')
                return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['code_confirm']})
            else:
                return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_pass']})
        else:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']})
    except NotImplementedError:
        current_password = request.POST.get('old_pass')
        user = User.objects.get(email=request.POST.get('email'))
        print(user.check_password(current_password))
        if not user.check_password(current_password):
            email = request.POST.get('email')
            code = ''
            for i in range(6):
                code += str(random.randint(0, 9))
            cache.set(email, code, 300)
            send_verification_email.delay(email, code, 'reset')
            return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['code_confirm']})
        else:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_pass']})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def change_password(request):
    try:
        if request.method == 'POST':
            code = cache.get(request.user.email)
            if code == request.POST.get('code'):
                new_password = request.POST.get('password')
                request.user.set_password(new_password)
                request.user.save()
                login(request, request.user)
                return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['changed_pass']})
            else:
                return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_code']})
        else:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']})
    except AttributeError:
        email = request.POST.get('email')
        code = cache.get(email)
        if code == request.POST.get('code'):
            new_password = request.POST.get('password')
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            login(request, user)
            return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['changed_pass']})
        else:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_code']})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def user_login(request):
    try:
        if request.user.is_anonymous:
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['auth']}, safe=False)
            else:
                return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_credentials']}, safe=False)
        else:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']}, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, safe=False)


def google_auth(request):
    try:
        redirect_uri = request.build_absolute_uri(reverse('google_callback'))
        params = {
            'response_type': 'code',
            'scope': 'email profile',
            'redirect_uri': redirect_uri,
            'client_id': settings.GOOGLE_CLIENT_ID,
        }
        url = 'https://accounts.google.com/o/oauth2/auth?' + urllib.parse.urlencode(params)
        return redirect(url)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


def google_callback(request):
    if 'error' in request.GET:
        return HttpResponseBadRequest(request.GET['error_description'])
    else:
        try:
            code = request.GET.get('code', None)
            if code is None:
                return HttpResponseBadRequest('No code provided')
            else:
                redirect_uri = request.build_absolute_uri(reverse('google_callback'))
                data = {
                    'code': code,
                    'redirect_uri': redirect_uri,
                    'client_id': settings.GOOGLE_CLIENT_ID,
                    'client_secret': settings.GOOGLE_CLIENT_SECRET,
                    'grant_type': 'authorization_code',
                }
                response = requests.post('https://accounts.google.com/o/oauth2/token', data=data)
                if response.status_code != 200:
                    return HttpResponseBadRequest(response.text)
                else:
                    tokens = json.loads(response.text)
                    access_token = tokens['access_token']
                    id_token = tokens['id_token']
                    user_info = requests.get('https://www.googleapis.com/oauth2/v1/userinfo?access_token=' + access_token)
                    user_info = json.loads(user_info.text)
                    if GoogleCredentials.objects.filter(email=user_info['email']):
                        user, created = CustomUser.objects.get_or_create(email=user_info['email'])
                        if user is not None:
                            login(request, user)
                            return redirect('index')
                        else:
                            return HttpResponse('Authentication failed')
                    else:
                        try:
                            user = CustomUser.objects.get(email=user_info['email'])
                        except CustomUser.DoesNotExist:
                            user = CustomUser.objects.create(email=user_info['email'], is_registered_via_google=True)
                        credentials = GoogleCredentials.objects.create(user=user, access_token=access_token,
                                                                       id_token=id_token, email=user_info['email'])
                        credentials.save()
                        if user is not None:
                            login(request, user)
                            return redirect('index')
                        else:
                            return HttpResponse('Authentication failed')
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def registration_code(request):
    email = request.POST.get('email')
    try:
        User.objects.get(email=email)
        return JsonResponse({'success': False, 'message': ERROR_MESSAGES['email_registered']}, safe=False)
    except User.DoesNotExist:
        try:
            code = ''
            for i in range(6):
                code += str(random.randint(0, 9))
            cache.set(email, code, 300)
            send_verification_email.delay(email, code, 'registration')
            return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['code_confirm']}, safe=False)
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)}, safe=False)


@csrf_exempt
def reg(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            email = request.POST.get('email')
            code = cache.get(email)
            user_code = request.POST.get('code')
            password = request.POST.get('password')

            if user_code == code:
                user = User.objects.create(email=email, username=username)
                user.set_password(password)
                user.save()
                return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['reg']}, safe=False)
            else:
                return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_code']}, safe=False)
        else:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['invalid_request']}, safe=False)
    except Exception as e:
        return JsonResponse({'success': True, 'message': str(e)})


def user_logout(request):
    logout(request)
    return redirect('login')


@csrf_exempt
def add_to_cart(request):
    try:
        beat_id = request.POST.get('beat_id')
        beat = Beat.objects.get(beat_id=beat_id)
        cart = request.session.get('cart', {})
        cart[beat_id] = {
            'id': beat.beat_id,
        }
        request.session['cart'] = cart
        return JsonResponse({'success': True}, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)}, safe=False)


def shopping_cart(request):
    try:
        cart = request.session.get('cart', {})
        print(cart)
        basic_license = License.objects.get(license_level=1)
        beat_license = License.objects.all()

        cart_items = []
        amount = 0
        for item in cart.values():
            beat = Beat.objects.get(beat_id=item['id'])
            price = beat.price + basic_license.price
            cart_items.append({
                'id': beat.beat_id,
                'title': beat.title,
                'cover': beat.cover,
                'type': beat.type,
                'tonal': beat.tonal,
                'bpm': beat.bpm,
                'price': price
            })
            amount += price
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
    context = {
        'cart': cart_items,
        'amount': amount,
        'license': beat_license
    }
    return render(request, 'user/shopping-cart.html', context)


def get_cart(request):
    try:
        cart = request.session.get('cart', {})
        selected_license = request.session.get('license', 'BASIC')  # Получение выбранной лицензии из сессии
        basic_license = License.objects.get(license_level=1)
        cart_items = []
        for item in cart.values():
            beat = Beat.objects.get(beat_id=item['id'])
            beat_price = beat.price
            if selected_license != 'BASIC':
                selected_license_obj = License.objects.get(name=selected_license)
                beat_price += selected_license_obj.price
            cart_items.append({
                'id': beat.beat_id,
                'title': str(beat.title),
                'cover': str(beat.cover),
                'type': str(beat.type),
                'tonal': str(beat.tonal),
                'bpm': str(beat.bpm),
                'price': beat_price
            })
        data = json.dumps(cart_items)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'success': True, 'message': str(e)})

def get_license(request):
    try:
        beat_license = License.objects.all()
        data = serializers.serialize('json', list(beat_license))
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'success': True, 'message': str(e)})


@csrf_exempt
def license_improvement(request):
    try:
        beat_id = request.POST.get('beat_id')
        beat_item = OrderItems.objects.get(beat_id=beat_id)
        max_license_level = License.objects.aggregate(Max('license_level'))['license_level__max']

        if beat_item.license.license_level != max_license_level:
            higher_license = License.objects.filter(license_level__gt=beat_item.license.license_level).first()
            beat_item.license = higher_license
            beat_item.save()

            beat_data = {
                'beat_id': beat_item.beat.beat_id,
                'title': beat_item.beat.title,
                'cover': beat_item.beat.cover,
                'created_at': beat_item.order_id.created_at.isoformat(),
                'type': beat_item.beat.type.title,
                'tonal': beat_item.beat.tonal.title,
                'bpm': beat_item.beat.bpm,
                'license': beat_item.license.name,
                'price': beat_item.beat.price,
            }
            return JsonResponse({'success': True, 'beats': beat_data, 'message': SUCCESS_MESSAGES['improve_license']})
        else:
            return JsonResponse({'success': False, 'message': ERROR_MESSAGES['max_level']})
    except OrderItems.DoesNotExist:
        return JsonResponse({'success': False, 'message': ERROR_MESSAGES['order_not_exist']})
    except License.DoesNotExist:
        return JsonResponse({'success': False, 'message': ERROR_MESSAGES['license_not_exist']})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def delete_item(request):
    try:
        beat_id = request.POST.get('beat_id')
        cart = request.session.get('cart', {})
        item_found = False
        for key, item in cart.items():
            if item['id'] == int(beat_id):
                del cart[key]
                request.session['cart'] = cart
                item_found = True
                break
        if item_found:
            return JsonResponse({'success': True}, safe=False)
        else:
            return JsonResponse({'success': False}, safe=False)
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})


@csrf_exempt
def create_order(request):
    try:
        transaction = request.POST.get('transaction_id')
        status = request.POST.get('status')
        get_license = request.POST.get('license')
        beat_license = License.objects.get(name=get_license)
        cart = request.session.get('cart', {})
        if status == "COMPLETED":
            try:
                order = Order.objects.create(transaction_id=transaction, user_id=request.user, status=status)
                for item in cart.values():
                    beat = Beat.objects.get(beat_id=item['id'])
                    OrderItems.objects.create(order_id=order, beat=beat, license=beat_license, amount=beat.price)
                del request.session['cart']
            except Exception as e:
                Order.objects.create(transaction_id=transaction, user_id=request.user, status=str(e))
        else:
            Order.objects.create(transaction_id=transaction, user_id=request.user, status=status)
        return JsonResponse({'success': True, 'message': SUCCESS_MESSAGES['order_created']})
    except Exception as e:
        return JsonResponse({'success': True, 'message': str(e)})
