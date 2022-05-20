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
    Category,
)
from .forms import (
    CategoryForm
)

from django.utils import timezone
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'


class Category_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/category.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Category"
        return context

class Category_Create(LoginRequiredMixin,TemplateView):
    template_name = 'components/category_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Category"
        return context

class Category_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/category_forms.html'
    def get(self, request):
        data = dict()
        form = CategoryForm()
        context = {
            'form': form,
            'is_Create': True,
            'btn_name': "primary",
            'btn_title': "Submit & Save",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)
    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            form = CategoryForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                data['url'] = reverse('category')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'
        return JsonResponse(data)

class Category_Update(LoginRequiredMixin,TemplateView):
    template_name = 'components/category_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['category'] = Category.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Category"
        return context

class Category_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/category_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        category = Category.objects.get(pk=id)
        form = CategoryForm(instance=category)
        context = {
            'form': form,
            'category':category,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Save Changes",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Category_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        category = Category.objects.get(pk=pk)
        if request.method == 'POST':
            form = CategoryForm(request.POST,request.FILES,instance=category)
            if form.is_valid():
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('category')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'

        return JsonResponse(data)

class Category_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Category.objects.all()
    template_name = 'tables/category_table.html'
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
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(Q(category__icontains = search)).count()
            category = self.queryset.filter(Q(category__icontains = search)).order_by('category')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'category':category,'start':start})
        return JsonResponse(data)
