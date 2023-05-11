import json
import uuid
import random
import requests
import urllib.parse
from index.models import Beat
from django.urls import reverse
from django.conf import settings
from .forms import CreateUserForm
from django.contrib import messages
from django.core.cache import cache
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .models import CustomUser, GoogleCredentials
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseBadRequest, HttpResponse, JsonResponse


def user_login(request):
    if request.user.is_anonymous:
        if request.method == 'POST':
            email = request.POST.get("email")
            password = request.POST.get("password")

            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                return redirect('/')
            else:
                messages.info(request, "Username or password is incorrect")
    else:
        return redirect('/')
    return render(request, 'user/login.html')


def user_reg(request):
    if request.user.is_anonymous:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
    else:
        return redirect('/')
    context = {
        'form': form
    }
    return render(request, 'user/registration.html', context)


def google_auth(request):
    redirect_uri = request.build_absolute_uri(reverse('google_callback'))
    params = {
        'response_type': 'code',
        'scope': 'email profile',
        'redirect_uri': redirect_uri,
        'client_id': settings.GOOGLE_CLIENT_ID,
    }
    url = 'https://accounts.google.com/o/oauth2/auth?' + urllib.parse.urlencode(params)
    return redirect(url)


def google_callback(request):
    if 'error' in request.GET:
        return HttpResponseBadRequest(request.GET['error_description'])
    else:
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
                        return redirect('/')
                    else:
                        return HttpResponse('Authentication failed')
                else:
                    user, created = CustomUser.objects.get_or_create(email=user_info['email'])
                    credentials = GoogleCredentials.objects.create(user=user, access_token=access_token,
                                                                   id_token=id_token, email=user_info['email'])
                    credentials.save()
                    if user is not None:
                        login(request, user)
                        return redirect('/')
                    else:
                        return HttpResponse('Authentication failed')


def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            code = ''
            token = str(uuid.uuid4())
            for i in range(6):
                code += str(random.randint(0, 9))
            print(code)
            cache.set(email, code, 300)
            cache.set(token, token, 300)
            send_verification_email(email, code)
            return redirect('confirmEmail', email, token)
        except:
            messages.info(request, 'Not found email!')
    return render(request, 'user/reset_password.html')


def send_verification_email(email, code):
    subject = 'Email verification code'
    message = render_to_string('user/verification_email.html', {'code': code})
    recipient_list = [email]
    send_mail(subject, message, settings.EMAIL_HOST, recipient_list, fail_silently=False)


def confirm_email(request, email, token):
    code = cache.get(email)
    get_token = cache.get(token)
    if get_token == token:
        if request.method == 'POST':
            if code == request.POST.get('code'):
                return redirect('changePassword', email, token)
    else:
        return redirect('login')
    return render(request, 'user/confirm_email.html')


def change_password(request, email, token):
    get_token = cache.get(token)
    if get_token == token:
        if request.method == 'POST':
            new_password = request.POST.get('password')
            if len(new_password) >= 6:
                user = CustomUser.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return redirect('login')
            else:
                print('Password invalid')
    else:
        return redirect('auth')
    return render(request, 'user/changePassword.html')


@login_required(login_url='login')
def user_profile(request):
    return render(request, 'user/cab.html')


def user_logout(request):
    logout(request)
    return redirect('login')


def add_to_cart(request, beat_id):
    beat = Beat.objects.get(beat_id=beat_id)
    cart = request.session.get('cart', {})
    cart[beat_id] = {
        'id': beat.beat_id,
    }
    request.session['cart'] = cart

    return redirect('shop_cart')


def shopping_cart(request):
    cart = request.session.get('cart', {})

    cart_items = []
    amount = 0
    for item in cart.values():
        beat = Beat.objects.get(beat_id=item['id'])
        cart_items.append({
            'id': beat.beat_id,
            'title': beat.title,
            'cover': beat.cover,
            'type': beat.type,
            'tonal': beat.tonal,
            'bpm': beat.bpm,
            'price': beat.price
        })
        amount += beat.price
    context = {
        'cart': cart_items,
        'amount': amount
    }
    return render(request, 'user/shopping-cart.html', context)


def get_cart(request):
    cart = request.session.get('cart', {})
    cart_items = []
    for item in cart.values():
        beat = Beat.objects.get(beat_id=item['id'])
        cart_items.append({
            'id': beat.beat_id,
            'title': str(beat.title),
            'cover': str(beat.cover),
            'type': str(beat.type),
            'tonal': str(beat.tonal),
            'bpm': str(beat.bpm),
            'price': str(beat.price)
        })
    data = json.dumps(cart_items)
    return JsonResponse(data, safe=False)


@csrf_exempt
def delete_item(request, pk):
    cart = request.session.get('cart', {})
    item_found = False
    for key, item in cart.items():
        if item['id'] == pk:
            del cart[key]
            request.session['cart'] = cart
            item_found = True
            break

    if item_found:
        return JsonResponse({'success': True}, safe=False)
    else:
        return JsonResponse({'success': False}, safe=False)
