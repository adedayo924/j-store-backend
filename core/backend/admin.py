from django.contrib import admin
from django.contrib.admin import register

from backend.models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'fullname', 'created_at']
    readonly_fields = ['password']

