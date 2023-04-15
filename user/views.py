
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import render_to_string

from .forms import CreateUserForm
from django.urls import reverse
from django.conf import settings
import urllib.parse
from .models import CustomUser, GoogleCredentials
from django.http import HttpResponseBadRequest, HttpResponse
import requests
import json
import uuid
import random
from django.core.cache import cache
from django.core.mail import send_mail

# Create your views here.

def userLogin(request):
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

def userReg(request):
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
                    credentials = GoogleCredentials.objects.create(user=user, access_token=access_token, id_token=id_token, email=user_info['email'])
                    credentials.save()
                    if user is not None:
                        login(request, user)
                        return redirect('/')
                    else:
                        return HttpResponse('Authentication failed')
                return redirect('/')

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
    getToken = cache.get(token)
    if getToken == token:
        if request.method == 'POST':
            if code == request.POST.get('code'):
                return redirect('changePassword', email, token)
    else:
        return redirect('login')
    return render(request, 'user/confirm_email.html')

def change_password(request, email, token):
    getToken = cache.get(token)
    if getToken == token:
        if request.method == 'POST':
            newPassword = request.POST.get('password')
            if len(newPassword) >= 6:
                user = CustomUser.objects.get(email=email)
                user.set_password(newPassword)
                user.save()
                return redirect('login')
            else:
                print('Password invalid')
    else:
        return redirect('auth')
    return render(request, 'user/changePassword.html')