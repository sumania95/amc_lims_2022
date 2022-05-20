from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
)

#functions
from django.db.models.functions import Coalesce,Concat
from django.db.models import Q,F,Sum,Count
from django.db.models import Value
from django.urls import reverse
#datetime
from datetime import datetime
#JSON AJAX
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView

from .forms import CustomAuthenticationForm
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'

class Login(LoginView):
    template_name = 'authentication/login.html'
    form_class = CustomAuthenticationForm

    def get_success_url(self,*args,**kwargs):
        return reverse('dashboard')

class Logout(LoginRequiredMixin,View):
    login_url = 'login'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        logout(request)
        return redirect('login')
