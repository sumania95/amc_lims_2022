from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from application.models import (
    User_Type
)
class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        print(user)
        if not User_Type.objects.filter(user__username = user.username):
            raise forms.ValidationError('Please enter a correct username and password. Note that both fields may be case-sensitive.', code='invalid_login')
        if User_Type.objects.filter(user__username = user.username, is_active = False):
            raise forms.ValidationError('Your Account has been deactivate. Contact Your Administrator', code='invalid_login')
