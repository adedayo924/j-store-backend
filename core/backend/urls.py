from django.urls import path

from backend.views import create_account

urlpatterns = [
    path('create_account/', create_account),
]
