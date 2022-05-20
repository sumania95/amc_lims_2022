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
    Year_Term,
)
from .forms import (
    Year_TermForm
)
from django.db import transaction

from django.utils import timezone
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'


class Year_Term_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/year.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Year_Term"
        return context

class Year_Term_Create(LoginRequiredMixin,TemplateView):
    template_name = 'components/year_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Year_Term"
        return context

class Year_Term_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/year_forms.html'
    def get(self, request):
        data = dict()
        form = Year_TermForm()
        context = {
            'form': form,
            'is_Create': True,
            'btn_name': "primary",
            'btn_title': "Submit & Save",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

    @transaction.atomic
    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            form = Year_TermForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                data['url'] = reverse('year')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'
        return JsonResponse(data)

class Year_Term_Update(LoginRequiredMixin,TemplateView):
    template_name = 'components/year_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['year'] = Year_Term.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Year_Term"
        return context

class Year_Term_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/year_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        year = Year_Term.objects.get(pk=id)
        form = Year_TermForm(instance=year)
        context = {
            'form': form,
            'year':year,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "Save Changes",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Year_Term_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        year = Year_Term.objects.get(pk=pk)
        if request.method == 'POST':
            form = Year_TermForm(request.POST,request.FILES,instance=year)
            if form.is_valid():
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('year')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'

        return JsonResponse(data)

class Year_Term_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Year_Term.objects.all()
    template_name = 'tables/year_table.html'
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
            data['counter'] = self.queryset.filter(Q(year_term__icontains = search)).count()
            year_term = self.queryset.filter(Q(year_term__icontains = search)).order_by('year_term')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'year':year_term,'start':start})
        return JsonResponse(data)
