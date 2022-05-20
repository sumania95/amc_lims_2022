from django import forms
from django.forms import ModelForm
from application.models import (
    Author,
)

class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = [
            'lastname',
            'firstname',
            'middlename',
            'ext_name',
        ]
