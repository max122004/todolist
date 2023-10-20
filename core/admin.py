from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from core.models import User
from .forms import CustomUserChangeForm


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm


admin.site.register(User, CustomUserAdmin)
