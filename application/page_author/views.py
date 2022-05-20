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
from application.models import (
    Author,
)
from .forms import (
    AuthorForm
)

from django.utils import timezone
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'


class Author_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/author/page_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Author"
        context['URL_CREATE'] = reverse('author_create')
        context['URL_TABLE'] = reverse('author_table_api')
        return context

class Author_Create(LoginRequiredMixin,TemplateView):
    template_name = 'pages/author/x_page_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Author"
        context['NAV_ACTIVE'] = "author_active"
        context['URL_CREATE'] = reverse('author_create_api')
        return context

class Author_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'pages/author/page_forms.html'
    def get(self, request):
        data = dict()
        form = AuthorForm()
        context = {
            'form': form,
            'is_Create': True,
            'btn_name': "primary",
            'btn_submit': "button-submit",
            'btn_title': "Submit & Save",
            'URL_CREATE_UPDATE' : reverse('author_create_api')

        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)
    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            form = AuthorForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                data['url'] = reverse('author')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'
        return JsonResponse(data)

class Author_Update(LoginRequiredMixin,TemplateView):
    template_name = 'pages/author/x_page_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['author'] = Author.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Author"
        context['URL_UPDATE'] = reverse('author_update_api')
        return context

class Author_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'pages/author/page_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        author = Author.objects.get(pk=id)
        form = AuthorForm(instance=author)
        print(id)
        context = {
            'is_Create': False,
            'form': form,
            'btn_name': "warning",
            'btn_submit': "button-change",
            'btn_title': "Save Changes",
            'URL_CREATE_UPDATE' : reverse('author_update_save_api',kwargs={'pk': id})
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Author_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        author = Author.objects.get(pk=pk)
        if request.method == 'POST':
            form = AuthorForm(request.POST,request.FILES,instance=author)
            if form.is_valid():
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('author')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'

        return JsonResponse(data)

class Author_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Author.objects.all()
    template_name = 'pages/author/x_page_table.html'
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
            URL_UPDATE = reverse('author')
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(Q(lastname__icontains = search)|Q(firstname__icontains = search)).count()
            record = self.queryset.filter(Q(lastname__icontains = search)|Q(firstname__icontains = search)).order_by('lastname','firstname')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'record':record,'start':start,'URL_UPDATE':URL_UPDATE})
        return JsonResponse(data)
