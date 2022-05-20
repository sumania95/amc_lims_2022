from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from application.models import(
    User_Type
)
class UserForm(forms.ModelForm):
    last_name = forms.CharField()
    first_name = forms.CharField()
    class Meta:
        model = User
        fields = [
            'last_name',
            'first_name',
            'username',
            'password',
        ]

class User_TypeForm(forms.ModelForm):
    class Meta:
        model = User_Type
        fields = [
            'classification',
        ]
