from django.contrib import admin
from django.contrib.admin import register

from backend.models import User, Otp


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone', 'fullname', 'created_at']
    readonly_fields = ['password']


@register(Otp)
class OtpAdmin(admin.ModelAdmin):
    list_display = ['phone', 'otp', 'validity', 'verified']
