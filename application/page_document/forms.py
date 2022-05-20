from django import forms
from django.forms import ModelForm
from application.models import (
    Document,
)

class DocumentForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 3,'style' : "white-space: pre-wrap"},))
    remarks = forms.CharField(widget=forms.Textarea(attrs={'rows': 3,'style' : "white-space: pre-wrap"},),required=False)
    class Meta:
        model = Document
        fields = [
            'document_type',
            'series_no',
            'description',
            'category',
            'file',
            'date_enacted',
            'date_approved',
            'remarks'
        ]
