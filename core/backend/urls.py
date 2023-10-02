from django.urls import path

from backend.views import request_otp

urlpatterns = [
    path('request_otp/', request_otp),
]
