from django.urls import path

from backend.views import request_otp, verify_otp, create_account, login

urlpatterns = [
    path('request_otp/', request_otp),
    path('verify_otp/', verify_otp),
    path('create_account/', create_account),
    path('login/', login)
]
