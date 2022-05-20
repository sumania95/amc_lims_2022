from django import forms
from django.forms import ModelForm
from application.models import (
    Year_Term,
)

class Year_TermForm(forms.ModelForm):
    class Meta:
        model = Year_Term
        fields = [
            'year_term',
        ]
