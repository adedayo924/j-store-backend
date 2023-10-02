from rest_framework.decorators import api_view
from rest_framework.response import Response

from backend.models import User
from backend.utils import send_otp


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
