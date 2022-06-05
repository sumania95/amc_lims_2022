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
    Document,
    Author,
    Document_Author,
    Document_Author_Abstract,
    Document_Type
)
from .forms import (
    DocumentForm
)
from django.db import transaction

from django.utils import timezone
success = 'success'
info = 'info'
error = 'error'
warning = 'warning'
question = 'question'


class Document_Page(LoginRequiredMixin,TemplateView):
    template_name = 'pages/document.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Document"
        context['document_type'] = Document_Type.objects.all().order_by('document_type')
        return context

class Document_Create(LoginRequiredMixin,TemplateView):
    template_name = 'components/document_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "New Document"
        return context

class Document_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/document_forms.html'
    def get(self, request):
        data = dict()
        form = DocumentForm()
        context = {
            'form': form,
            'is_Create': True,
            'btn_name': "success",
            'btn_title': "PUBLISH NOW",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

    @transaction.atomic
    def post(self, request):
        data =  dict()
        if request.method == 'POST':
            form = DocumentForm(request.POST,request.FILES)
            if form.is_valid():
                form.instance.user = self.request.user
                document = form.save()
                document_author = Document_Author.objects.filter(user=self.request.user)
                for p in document_author:
                    Document_Author_Abstract.objects.create(document_id=document.id,author_id = p.author_id,user=self.request.user)
                Document_Author.objects.filter(user=self.request.user).delete()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully saved.'
                data['url'] = reverse('document')
            else:
                file = form.instance.file
                if not file.name.endswith('.pdf'):
                    data['valid'] = False
                    data['message_type'] = error
                    data['message_title'] = 'Please upload pdf file only.'
                else:
                    data['valid'] = False
                    data['message_type'] = error
                    data['message_title'] = 'Error connection found.'
        return JsonResponse(data)

class Document_Update(LoginRequiredMixin,TemplateView):
    template_name = 'components/document_update.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            id = self.kwargs['pk']
            context['document'] = Document.objects.get(id = id)
        except Exception as e:
            pass
        context['title'] = "Update Document"
        return context

class Document_Update_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/document_update_forms.html'

    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        document = Document.objects.get(pk=id)
        form = DocumentForm(instance=document)
        context = {
            'form': form,
            'document':document,
            'is_Create': False,
            'btn_name': "warning",
            'btn_title': "PUBLISH CHANGES",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Document_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data = dict()
        document = Document.objects.get(pk=pk)
        if request.method == 'POST':
            form = DocumentForm(request.POST,request.FILES,instance=document)
            if form.is_valid():
                form.save()
                data['valid'] = True
                data['message_type'] = success
                data['message_title'] = 'Successfully updated.'
                data['url'] = reverse('document')
            else:
                file = form.instance.file
                if not file.name.endswith('.pdf'):
                    data['valid'] = False
                    data['message_type'] = error
                    data['message_title'] = 'Please upload pdf file only.'
                else:
                    data['valid'] = False
                    data['message_type'] = error
                    data['message_title'] = 'Error connection found.'

        return JsonResponse(data)

class Document_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Document.objects.all()
    template_name = 'tables/document_table.html'
    def get(self, request):
        data = dict()
        try:
            search = self.request.GET.get('search')
            year = self.request.GET.get('year')
            document_type = self.request.GET.get('document_type')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
        except KeyError:
            year = None
            document_type = None
            search = None
            start = None
            end = None
        document_array = []
        if document_type or search or start or end or year:
            if year == "ALL":
                data['form_is_valid'] = True
                data['counter'] = self.queryset.filter(Q(description__icontains = search),document_type_id = document_type).count()
                document = self.queryset.filter(Q(description__icontains = search),document_type_id = document_type).order_by('date_enacted','date_created')[int(start):int(end)]
                # start
                for p in document:


                    documents = {
                        'document' : Document.objects.get(id=p.id),
                        'document_author' : Document_Author_Abstract.objects.filter(document_id = p.id)
                    }
                    document_array.append(documents)
                # end
                data['data'] = render_to_string(self.template_name,{'document_array':document_array,'start':start})
            else:
                data['form_is_valid'] = True
                data['counter'] = self.queryset.filter(Q(description__icontains = search),document_type_id = document_type,date_approved__year = year).count()
                document = self.queryset.filter(Q(description__icontains = search),document_type_id = document_type,date_approved__year = year).order_by('date_enacted','date_created')[int(start):int(end)]
                # start
                for p in document:


                    documents = {
                        'document' : Document.objects.get(id=p.id),
                        'document_author' : Document_Author_Abstract.objects.filter(document_id = p.id)
                    }
                    document_array.append(documents)
                # end
                print(document_array)
                data['data'] = render_to_string(self.template_name,{'document_array':document_array,'start':start})
        return JsonResponse(data)


class Document_Author_View_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Author.objects.all()
    template_name = 'tables/document_author_view_table.html'
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
                data['counter'] = self.queryset.exclude(id__in = Document_Author.objects.values('author_id').filter(user=self.request.user)).filter(Q(lastname__icontains = search)).count()
                document = self.queryset.exclude(id__in = Document_Author.objects.values('author_id').filter(user=self.request.user)).filter(Q(lastname__icontains = search)).order_by('lastname')[int(start):int(end)]
                data['data'] = render_to_string(self.template_name,{'document':document,'start':start})
            except Exception as e:
                raise
        return JsonResponse(data)

class Document_Author_Update_View_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Author.objects.all()
    template_name = 'tables/document_author_update_view_table.html'
    def get(self, request):
        data = dict()
        try:
            document_id = self.request.GET.get('document_id')
            search = self.request.GET.get('search')
            start = self.request.GET.get('start')
            end = self.request.GET.get('end')
        except KeyError:
            document_id = None
            search = None
            start = None
            end = None
        print(search)
        if search or start or end or id:
            try:
                data['form_is_valid'] = True
                data['counter'] = self.queryset.exclude(id__in = Document_Author_Abstract.objects.values('author_id').filter(document_id=document_id)).filter(Q(lastname__icontains = search)).count()
                author = self.queryset.exclude(id__in = Document_Author_Abstract.objects.values('author_id').filter(document_id=document_id)).filter(Q(lastname__icontains = search)).order_by('lastname')[int(start):int(end)]
                data['data'] = render_to_string(self.template_name,{'author':author,'start':start,'document_id':document_id})
            except Exception as e:
                raise
        return JsonResponse(data)

class Document_Author_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Document_Author.objects.all()
    template_name = 'tables/document_author_table.html'
    def get(self, request):
        data = dict()
        try:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(user=self.request.user).count()
            document = self.queryset.filter(user=self.request.user).order_by('author__lastname')
            data['data'] = render_to_string(self.template_name,{'document':document})
        except Exception as e:
            raise
        return JsonResponse(data)

class Document_Author_Update_Table_AJAXView(LoginRequiredMixin,View):
    queryset = Document_Author_Abstract.objects.all()
    template_name = 'tables/document_author_update_table.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        try:
            data['form_is_valid'] = True
            data['counter'] = self.queryset.filter(document_id=id).count()
            document = self.queryset.filter(document_id=id).order_by('author__lastname')
            data['data'] = render_to_string(self.template_name,{'document':document})
        except Exception as e:
            raise
        return JsonResponse(data)

class Document_Author_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/document_author_forms.html'
    def get(self, request):
        data = dict()
        context = {
            'title': "LIST OF AUTHORS",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Document_Author_Update_Create_AJAXView(LoginRequiredMixin,View):
    template_name = 'forms/document_author_update_forms.html'
    def get(self, request):
        data = dict()
        try:
            id = self.request.GET.get('id')
        except KeyError:
            id = None
        document = Document.objects.get(id=id)
        context = {
            'document':document,
            'title': "LIST OF AUTHORS",
        }
        data['html_form'] = render_to_string(self.template_name,context)
        return JsonResponse(data)

class Document_Author_Create_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data =  dict()

        try:
            author = Author.objects.get(pk=pk)
            if request.method == 'POST':
                Document_Author.objects.create(author=author,user=self.request.user)
                data['message_type'] = success
                data['message_title'] = 'Successfully added.'
        except Exception as e:
            raise
        return JsonResponse(data)

class Document_Author_Update_Create_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data =  dict()
        try:
            id = self.request.POST.get('document_id')
        except Exception as e:
            id = None
        print(id)
        try:
            author = Author.objects.get(pk=pk)
            if request.method == 'POST':
                Document_Author_Abstract.objects.create(document_id=id,author=author,user=self.request.user)
                data['message_type'] = success
                data['message_title'] = 'Successfully added.'
        except Exception as e:
            raise
        return JsonResponse(data)

class Document_Author_Remove_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data =  dict()
        try:
            if request.method == 'POST':
                Document_Author.objects.get(pk=pk).delete()
                data['message_type'] = success
                data['message_title'] = 'Successfully removed.'
        except Exception as e:
            raise
        return JsonResponse(data)

class Document_Author_Remove_Update_Save_AJAXView(LoginRequiredMixin,View):
    def post(self, request,pk):
        data =  dict()
        try:
            if request.method == 'POST':
                Document_Author_Abstract.objects.get(pk=pk).delete()
                data['message_type'] = success
                data['message_title'] = 'Successfully removed.'
        except Exception as e:
            raise
        return JsonResponse(data)
