import datetime
import uuid
from random import randint

from django.core.mail import EmailMessage
from django.template.loader import get_template
from rest_framework.response import Response

from backend.models import Otp, Token, PasswordResetToken
from core.settings import TEMPLATES_BASE_URL


def send_otp(phone):
    otp = randint(100000, 999999)
    validity = datetime.datetime.now() + datetime.timedelta(minutes=10)
    Otp.objects.update_or_create(phone=phone, defaults={"otp": otp, "verified": False, "validity": validity})

    # todo sms api
    print(otp)
    return Response('otp sent successfully')


def new_token():
    token = uuid.uuid1().hex
    return token


def token_response(user):
    token = new_token()
    Token.objects.create(token=token, user=user)
    return Response('token '+token)


def send_password_reset_email(user):
    token = new_token()
    exp_time = datetime.datetime.now() + datetime.timedelta(minutes=10)

    PasswordResetToken.objects.update_or_create(user=user, defaults={'user': user, 'token': token, 'validity': exp_time})

    email_data = {
        'token': token,
        'email': user.email,
        'base_url': TEMPLATES_BASE_URL
    }

    message = get_template('emails/reset-password.html').render(email_data)

    msg = EmailMessage('Reset Password', body=message, to=[user.email,])
    msg.content_subtype = 'html'

    try:
        msg.send()
    except:
        pass
    return Response('reset_password_email_sent')