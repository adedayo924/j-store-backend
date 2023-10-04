import datetime

from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from backend.models import User, Otp, PasswordResetToken, Token
from backend.utils import send_otp, token_response, send_password_reset_email
from core.settings import TEMPLATES_BASE_URL


@api_view(['POST'])
def request_otp(request):
    email = request.data.get('email')
    phone = request.data.get('phone')

    if email and phone:
        if User.objects.filter(email=email).exists():
            return Response('email already exists', status=400)
        if User.objects.filter(phone=phone).exists():
            return Response('phone number already exists', status=400)
        return send_otp(phone)
    else:
        return Response('data_missing', status=400)


@api_view(['POST'])
def verify_otp(request):
    phone = request.data.get('phone')
    otp = request.data.get('otp')

    otp_obj = get_object_or_404(Otp, phone=phone, verified=False)

    if otp_obj.validity.replace(tzinfo=None) > datetime.datetime.utcnow():
        if otp_obj.otp == otp:
            otp_obj.verified = True
            otp_obj.save()
            return Response('otp_verified_successfully')
        else:
            return Response('Incorrect otp', 400)
    else:
        return Response('Otp expired', 400)


@api_view(['POST'])
def create_account(request):
    email = request.data.get('email')
    phone = request.data.get('phone')
    fullname = request.data.get('fullname')
    password = request.data.get('password')

    if email and phone and fullname and password:
        otp_obj = get_object_or_404(Otp, phone=phone, verified=True)
        otp_obj.delete()

        User.objects.create(email=email, phone=phone, fullname=fullname, password=make_password(password))
        return Response('account created successfully!')
    else:
        return Response('data_missng', 400)


@api_view(['POST'])
def login(request):
    email = request.data.get('email')
    phone = request.data.get('phone')
    password = request.data.get('password')

    if email:
        user = get_object_or_404(User, email=email)
    elif phone:
        user = get_object_or_404(User, phone=phone)
    else:
        return Response('data_missing', 400)

    if check_password(password, user.password):
        return token_response(user)
    else:
        return Response('incorrect password', 400)


@api_view(['POST'])
def password_reset_email(request):
    email = request.data.get('email')
    if not email:
        return Response('params_missing', 400)

    user = get_object_or_404(User, email=email)
    return send_password_reset_email(user)


@api_view(['GET'])
def password_reset_form(request, email, token):
    token_instance = PasswordResetToken.objects.filter(user__email=email, token=token).first()
    link_expired = get_template('pages/link-expired.html').render()
    if token_instance:
        if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
            return  render(request, 'pages/new-password-form.html', {
                'email': email,
                'token': token,
                'base_url': TEMPLATES_BASE_URL
            })
        else:
            token_instance.delete()
            return HttpResponse(link_expired)
    else:
        return HttpResponse(link_expired)


@api_view(['POST'])
def password_reset_confirm(request):
    email = request.data.get('email')
    token = request.data.get('token')
    password1 = request.data.get('password1')
    password2 = request.data.get('password2')

    token_instance = PasswordResetToken.objects.filter(user__email=email, token=token).first()
    link_expired = get_template('pages/link-expired.html').render()

    if token_instance:
        if datetime.datetime.utcnow() < token_instance.validity.replace(tzinfo=None):
            if len(password1) < 8:
                return render(request, 'pages/new-password-form.html', {
                    'email': email,
                    'token': token,
                    'base_url': TEMPLATES_BASE_URL,
                    'error': 'Password length must be at least 8 characters!'
                })

            if password1 == password2:
                user = token_instance.user
                user.password = make_password(password1)
                user.save()
                token_instance.delete()
                Token.objects.filter(user=user).delete()
                return render(request, 'pages/password-updated.html')
            else:
                return render(request, 'pages/new-password-form.html', {
                    'email': email,
                    'token': token,
                    'base_url': TEMPLATES_BASE_URL,
                    'error': 'Password doesn\'t matched!'
                })
        else:
            token_instance.delete()
            return HttpResponse(link_expired)
    else:
        return HttpResponse(link_expired)

    print(password2)
    return Response('updated')
