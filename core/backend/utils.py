import datetime
import uuid
from random import randint

from rest_framework.response import Response

from backend.models import Otp, Token


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
