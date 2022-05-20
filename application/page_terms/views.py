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
    Terms,
    Author,
    Terms_Author,
    Terms_Author_Abstract,
)
from .forms import (
    TermsForm
)

from django.utils import timezone
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'


class Terms_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/terms/page_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Terms"
        context['URL_CREATE'] = reverse('terms_create')
        context['URL_TABLE'] = reverse('terms_table_api')
        return context

class Terms_Create(LoginRequiredMixin,TemplateView):
    template_name = 'pages/terms/x_page_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Terms"
        context['NAV_ACTIVE'] = "terms_active"
        context['URL_CREATE'] = reverse('terms_create_api')
        return context

class Terms_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'pages/terms/page_forms.html'
    def get(self, request):
        data = dict()
        form = TermsForm()
        context = {
            'form': form,
            'is_Create': True,
            'btn_name': "primary",
            'btn_submit': "button-submit",
            'btn_title': "Submit & Save",
            'URL_CREATE_UPDATE' : reverse('terms_create_api')

        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)
    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            form = TermsForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                terms = form.save()
                terms_author = Terms_Author.objects.filter(user=self.request.user)
                for p in terms_author:
                    Terms_Author_Abstract.objects.create(terms_id=terms.id,author_id = p.author_id,user=self.request.user)
                Terms_Author.objects.filter(user=self.request.user).delete()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                data['url'] = reverse('terms')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'
        return JsonResponse(data)

class Terms_Update(LoginRequiredMixin,TemplateView):
    template_name = 'pages/terms/x_page_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['terms'] = Terms.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Terms"
        context['URL_UPDATE'] = reverse('terms_update_api')
        return context

class Terms_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'pages/terms/page_update_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        terms = Terms.objects.get(pk=id)
        form = TermsForm(instance=terms)
        print(id)
        context = {
            'form': form,
            'terms':terms,
            'btn_name': "warning",
            'btn_submit': "button-change",
            'btn_title': "Save Changes",
            'URL_CREATE_UPDATE' : reverse('terms_update_save_api',kwargs={'pk': id})
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Terms_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        terms = Terms.objects.get(pk=pk)
        if request.method == 'POST':
            form = TermsForm(request.POST,request.FILES,instance=terms)
            if form.is_valid():
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('terms')
            else:
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = 'Error connection found.'

        return JsonResponse(data)

class Terms_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Terms.objects.all()
    template_name = 'pages/terms/x_page_table.html'
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
            URL_UPDATE = reverse('terms')
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(Q(description__icontains = search)).count()
            record = self.queryset.filter(Q(description__icontains = search)).order_by('description')[int(start):int(end)]
            data['data'] = render_to_string(self.template_name,{'record':record,'start':start,'URL_UPDATE':URL_UPDATE})
        return JsonResponse(data)

class Terms_Author_View_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Author.objects.all()
    template_name = 'pages/terms/x_page_author_view_table.html'
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
        print(search)
        if search or start or end:
            try:
                data['form_is_valid'] = True
                data['counter'] = self.queryset.exclude(id__in = Terms_Author.objects.values('author_id').filter(user=self.request.user)).filter(Q(lastname__icontains = search)).count()
                terms = self.queryset.exclude(id__in = Terms_Author.objects.values('author_id').filter(user=self.request.user)).filter(Q(lastname__icontains = search)).order_by('lastname')[int(start):int(end)]
                data['data'] = render_to_string(self.template_name,{'terms':terms,'start':start})
            except Exception as e:
                raise
        return JsonResponse(data)

class Terms_Author_Update_View_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Author.objects.all()
    template_name = 'pages/terms/x_page_author_update_view_table.html'
    def get(self, request):
        data = dict()
        try:
            terms_id = self.request.GET.get('terms_id')
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
        except KeyError:
            terms_id = None
            search = None
            start = None
            end = None
        print(search)
        if search or start or end or id:
            try:
                data['form_is_valid'] = True
                data['counter'] = self.queryset.exclude(id__in = Terms_Author_Abstract.objects.values('author_id').filter(terms_id=terms_id,user=self.request.user)).filter(Q(lastname__icontains = search)).count()
                author = self.queryset.exclude(id__in = Terms_Author_Abstract.objects.values('author_id').filter(terms_id=terms_id,user=self.request.user)).filter(Q(lastname__icontains = search)).order_by('lastname')[int(start):int(end)]
                data['data'] = render_to_string(self.template_name,{'author':author,'start':start,'terms_id':terms_id})
            except Exception as e:
                raise
        return JsonResponse(data)

class Terms_Author_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Terms_Author.objects.all()
    template_name = 'pages/terms/x_page_author_table.html'
    def get(self, request):
        data = dict()
        try:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(user=self.request.user).count()
            terms = self.queryset.filter(user=self.request.user).order_by('author__lastname')
            data['data'] = render_to_string(self.template_name,{'terms':terms})
        except Exception as e:
            raise
        return JsonResponse(data)

class Terms_Author_Update_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Terms_Author_Abstract.objects.all()
    template_name = 'pages/terms/x_page_author_update_table.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        print(id)
        try:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(terms_id=id,user=self.request.user).count()
            terms = self.queryset.filter(terms_id=id,user=self.request.user).order_by('author__lastname')
            data['data'] = render_to_string(self.template_name,{'terms':terms})
        except Exception as e:
            raise
        return JsonResponse(data)

class Terms_Author_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'pages/terms/x_page_author_forms.html'
    def get(self, request):
        data = dict()
        context = {
            'title': "LIST OF AUTHORS",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Terms_Author_Update_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'pages/terms/x_page_author_update_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        terms = Terms.objects.get(id=id)
        context = {
            'terms':terms,
            'title': "LIST OF AUTHORS",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Terms_Author_Create_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data =  dict()

        try:
            author = Author.objects.get(pk=pk)
            if request.method == 'POST':
                Terms_Author.objects.create(author=author,user=self.request.user)
                data['message_type'] = success
                data['message_title'] = 'Successfully added.'
        except Exception as e:
            raise
        return JsonResponse(data)

class Terms_Author_Update_Create_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data =  dict()
        try:
            id = self.request.POST.get('terms_id')
        except Exception as e:
            id = None
        print(id)
        try:
            author = Author.objects.get(pk=pk)
            if request.method == 'POST':
                Terms_Author_Abstract.objects.create(terms_id=id,author=author,user=self.request.user)
                data['message_type'] = success
                data['message_title'] = 'Successfully added.'
        except Exception as e:
            raise
        return JsonResponse(data)

class Terms_Author_Remove_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data =  dict()
        try:
            if request.method == 'POST':
                Terms_Author.objects.get(pk=pk).delete()
                data['message_type'] = success
                data['message_title'] = 'Successfully removed.'
        except Exception as e:
            raise
        return JsonResponse(data)

class Terms_Author_Remove_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data =  dict()
        try:
            if request.method == 'POST':
                Terms_Author_Abstract.objects.get(pk=pk).delete()
                data['message_type'] = success
                data['message_title'] = 'Successfully removed.'
        except Exception as e:
            raise
        return JsonResponse(data)
