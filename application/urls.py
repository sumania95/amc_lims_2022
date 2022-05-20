from django.urls import path,include
from .import views

from .views import (
    Home,
    Reports,
    Security_Page,
    Security_AJAXView,
    Document_PDF_Print,
    Summary_Terms_Document_PDF_Print,
)

urlpatterns = [
    path('', Home.as_view(), name = 'dashboard'),
    path('report/document/list', Document_PDF_Print.as_view(), name = 'document_list_report'),
    path('report/summary-terms/list', Summary_Terms_Document_PDF_Print.as_view(), name = 'summary_terms_report'),
    path('document/', include('application.page_document.urls')),
    path('author/', include('application.page_author.urls')),
    path('category/', include('application.page_category.urls')),
    path('terms/', include('application.page_terms.urls')),
    path('users/', include('application.page_users.urls')),
    path('reports/', Reports.as_view(), name = 'reports'),
    path('security/', Security_Page.as_view(), name = 'security'),
    path('api/security', Security_AJAXView.as_view(), name = 'api_security'),
]
