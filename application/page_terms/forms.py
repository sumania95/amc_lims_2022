from django import forms
from django.forms import ModelForm
from application.models import (
    Terms,
)

class TermsForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 2,'style' : "white-space: pre-wrap"},))
    class Meta:
        model = Terms
        fields = [
            'description',
            'date_from',
            'date_to',
        ]
