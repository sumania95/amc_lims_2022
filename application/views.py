from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import (
    View,
    TemplateView,
    ListView,
    DetailView,
)
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm,SetPasswordForm
from django.http import JsonResponse
from django.contrib.auth import update_session_auth_hash
import json
from django.contrib.auth import logout
#functions
from django.db.models.functions import Coalesce,Concat
from django.db.models import Q,F,Sum,Count
from django.db.models import Value
from django.urls import reverse
#datetime
from datetime import datetime
#JSON AJAX
from django.template.loader import render_to_string
from django.template import RequestContext
from django.contrib.auth.mixins import LoginRequiredMixin
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'

from django.utils import timezone
from application.render import (
    Render
)
from application.models import (
    Document,
    Document_Author_Abstract,
    Terms,
    Terms_Author_Abstract,
    Category,
    Document_Type,
    Author,
)
from django.contrib.auth.models import User

class Home(LoginRequiredMixin,TemplateView):
    template_name = 'pages/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document_count'] = Document.objects.count()
        context['category_count'] = Category.objects.count()
        context['author_count'] = Author.objects.count()
        context['terms_count'] = Terms.objects.count()
        total_size = Document.objects.all()
        size = 0
        for p in total_size:
            p.file.size
            size+=p.file.size
        context['total_size'] = size
        return context

class Reports(LoginRequiredMixin,TemplateView):
    template_name = 'pages/reports.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['document_type'] = Document_Type.objects.all().order_by('document_type')
        context['terms'] = Terms.objects.all().order_by('-description')
        return context

class Document_PDF_Print(LoginRequiredMixin,View):
    queryset = Document.objects.all()
    def get(self, request):
        try:
            document_type = self.request.GET.get('document_type')
            ddlyear = self.request.GET.get('ddlyear')
        except Exception as e:
            document_type = None
            ddlyear = None
        document_array = []
        document = self.queryset.filter(document_type = document_type,date_approved__year = ddlyear).order_by('date_approved')
        for p in document:


            documents = {
                'document' : Document.objects.get(id=p.id),
                'document_author' : Document_Author_Abstract.objects.filter(document_id = p.id)
            }
            document_array.append(documents)
        now = timezone.now()
        document_type_class = Document_Type.objects.get(id=document_type)
        params = {
            'now': now,
            'document_type': document_type_class,
            'ddlyear': ddlyear,
            'document': document_array,
        }
        pdf = Render.render('reports/document_PDF_print.html', params)
        return pdf

class Summary_Terms_Document_PDF_Print(LoginRequiredMixin,View):
    queryset = Terms.objects.all()
    def get(self, request):
        try:
            id = self.request.GET.get('id')
        except Exception as e:
            id = None
        summary_terms_array = []
        term = self.queryset.get(id = id)
        term_abstract = Terms_Author_Abstract.objects.filter(terms=term).order_by('author__lastname')
        for p in term_abstract:
            terms = {
                'author' : Author.objects.get(id=p.author.id),
                'code_count' : Document_Author_Abstract.objects.filter(author=p.author,document__date_approved__gte = term.date_from,document__date_approved__lte = term.date_to,document__document_type = Document_Type.objects.get(document_type="CODE")).count(),
                'ordinance_count' : Document_Author_Abstract.objects.filter(author=p.author,document__date_approved__gte = term.date_from,document__date_approved__lte = term.date_to,document__document_type = Document_Type.objects.get(document_type="ORDINANCE")).count(),
                'resolution_count' : Document_Author_Abstract.objects.filter(author=p.author,document__date_approved__gte = term.date_from,document__date_approved__lte = term.date_to,document__document_type = Document_Type.objects.get(document_type="RESOLUTION")).count(),
            }
            summary_terms_array.append(terms)
        now = timezone.now()
        params = {
            'now': now,
            'term': term,
            'summary_terms_array': summary_terms_array,
        }
        pdf = Render.render('reports/summary_terms_document_PDF_print.html', params)
        return pdf


class Security_Page(LoginRequiredMixin,TemplateView):
    LOGIN_URL = 'login'
    template_name = 'pages/security.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Change Password"
        return context

class Security_AJAXView(LoginRequiredMixin,View):
    def get(self, request):
        data = dict()
        user = User.objects.get(id=self.request.user.id)
        form = PasswordChangeForm(user=user)
        context = {
            'form': form,
            'user': user,
            'btn_name': "primary",
            'btn_title': "Submit",
        }
        data['html_form'] = render_to_string('forms/security_forms.html',context)
        return JsonResponse(data)

    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            form = PasswordChangeForm(user=self.request.user,data=request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('dashboard')
                logout(request)
            else:
                message = form.errors.as_json()
                y = json.loads(message)
                try:
                    title = y["new_password2"][0]["message"]
                except Exception as e:
                    pass
                try:
                    title = y["old_password"][0]["message"]
                except Exception as e:
                    pass
                print(message)
                data['valid'] = False
                data['message_type'] = error
                data['message_title'] = title

        return JsonResponse(data)
