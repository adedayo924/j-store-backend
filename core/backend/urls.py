from django.urls import path

from backend.views import request_otp, verify_otp, create_account, login, password_reset_email, password_reset_form, \
    password_reset_confirm

urlpatterns = [
    path('request_otp/', request_otp),
    path('verify_otp/', verify_otp),
    path('create_account/', create_account),
    path('login/', login),
    path('password_reset_email/', password_reset_email),
    path('password_reset_form/<email>/<token>/', password_reset_form, name="password_reset_form"),
    path('password_reset_confirm/', password_reset_confirm, name="password_reset_confirm"),
]
