from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['POST'])
def create_account(request):
    email = request.data.get('email')
    phone = request.data.get('phone')
    fullname = request.data.get('fullname')
    password = request.data.get('password')

    return Response('')
