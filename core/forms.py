from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        fields = ['username', 'email', 'first_name', 'last_name']


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm


