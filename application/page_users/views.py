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

from .forms import (
    UserForm,
    User_TypeForm
)
from application.models import (
    User_Type
)
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.utils import timezone
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'
from application.decorators import LogoutIfNotAdminMixin

class User_Page(LoginRequiredMixin,LogoutIfNotAdminMixin,TemplateView):
    template_name = 'pages/user/page_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "User"
        context['URL_CREATE'] = reverse('user_create')
        context['URL_TABLE'] = reverse('user_table_api')
        return context

class User_Create(LoginRequiredMixin,LogoutIfNotAdminMixin,TemplateView):
    template_name = 'pages/user/x_page_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New User"
        context['NAV_ACTIVE'] = "user_active"
        context['URL_CREATE'] = reverse('user_create_api')
        return context

class User_Create_AJAXView(LoginRequiredMixin,LogoutIfNotAdminMixin,View):
    template_name = 'pages/user/page_forms.html'
    def get(self, request):
        data = dict()
        form = UserForm()
        user_form = User_TypeForm()
        context = {
            'form': form,
            'user_form': user_form,
            'is_Create': True,
            'btn_name': "primary",
            'btn_submit': "button-submit",
            'btn_title': "Submit & Save",
            'URL_CREATE_UPDATE' : reverse('user_create_api')

        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)
    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            form = UserForm(request.POST,request.FILES)
            try:
                if form.is_valid():
                    new_user = form.save(commit=False)
                    username = form.cleaned_data['username'] # get password
                    password = form.cleaned_data['password'] # get password
                    authenticate(username=username, password=password)
                    new_user.set_password(password) # set the password
                    new_user.save() # save the user
                    print(new_user)
                    User_Type.objects.create(user=new_user)
                    data['valid'] = True
                    data['message_type'] = success
                    data['message_title'] = 'Successfully saved.'
                    data['url'] = reverse('user')
                else:
                    data['valid'] = False
                    data['message_type'] = error
                    data['message_title'] = 'Error connection found.'
            except Exception as e:
                raise

        return JsonResponse(data)

class User_Update(LoginRequiredMixin,TemplateView):
    template_name = 'pages/user/x_page_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['user'] = User.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update User"
        context['URL_UPDATE'] = reverse('user_update_api')
        return context

class User_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'pages/user/page_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        user = User.objects.get(pk=id)
        form = UserForm(instance=user)
        print(id)
        context = {
            'form': form,
            'btn_name': "warning",
            'btn_submit': "button-change",
            'btn_title': "Save Changes",
            'URL_CREATE_UPDATE' : reverse('user_update_save_api',kwargs={'pk': id})
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class User_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        user = User.objects.get(pk=pk)
        if request.method == 'POST':
            form = UserForm(request.POST,request.FILES,instance=user)
            if form.is_valid():
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('user')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'

        return JsonResponse(data)

class User_Table_AJAXView(LoginRequiredMixin,LogoutIfNotAdminMixin,View):
    queryset = User_Type.objects.all()
    template_name = 'pages/user/x_page_table.html'
    def get(self, request):
        data = dict()
        try:
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
        except KeyError:
            search = None
            start = None
            end = None
        if search or start or end:
            URL_UPDATE = reverse('user')
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(Q(user__last_name__icontains = search)|Q(user__first_name__icontains = search)).count()
            record = self.queryset.filter(Q(user__last_name__icontains = search)|Q(user__first_name__icontains = search)).order_by('user__last_name','user__first_name')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'record':record,'start':start,'URL_UPDATE':URL_UPDATE})
        return JsonResponse(data)
