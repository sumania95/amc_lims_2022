from django import forms
from django.forms import ModelForm
from application.models import (
    Category,
)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = [
            'category',
        ]
