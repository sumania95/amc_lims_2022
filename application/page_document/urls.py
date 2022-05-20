from django.urls import path,include
from .import views

from .views import (
    Document_Page,
    Document_Create,
    Document_Create_AJAXView,
    Document_Update,
    Document_Update_AJAXView,
    Document_Update_Save_AJAXView,
    Document_Table_AJAXView,
    Document_Author_Table_AJAXView,
    Document_Author_Update_Table_AJAXView,
    Document_Author_View_Table_AJAXView,
    Document_Author_Update_View_Table_AJAXView,
    Document_Author_Create_AJAXView,
    Document_Author_Update_Create_AJAXView,
    Document_Author_Create_Save_AJAXView,
    Document_Author_Update_Create_Save_AJAXView,
    Document_Author_Remove_Save_AJAXView,
    Document_Author_Remove_Update_Save_AJAXView
    # Document_Print,
)
# 127.0.0.1:8000/document/
urlpatterns = [
    path('', Document_Page.as_view(), name = 'document'),
    path('create', Document_Create.as_view(), name = 'document_create'),
    path('api/create', Document_Create_AJAXView.as_view(), name = 'document_create_api'),
    path('update/<uuid:pk>', Document_Update.as_view(), name = 'document_update'),
    path('api/update/', Document_Update_AJAXView.as_view(), name = 'document_update_api'),
    path('api/update/save/<uuid:pk>', Document_Update_Save_AJAXView.as_view(), name = 'document_update_save_api'),
    path('api/table', Document_Table_AJAXView.as_view(), name = 'document_table_api'),
    path('api/author/table', Document_Author_Table_AJAXView.as_view(), name = 'document_author_table_api'),
    path('api/author/table/update', Document_Author_Update_Table_AJAXView.as_view(), name = 'document_author_update_table_api'),
    path('api/author/table/view', Document_Author_View_Table_AJAXView.as_view(), name = 'document_author_view_table_api'),
    path('api/author/table/update/view', Document_Author_Update_View_Table_AJAXView.as_view(), name = 'document_author_update_view_table_api'),
    path('api/author/create', Document_Author_Create_AJAXView.as_view(), name = 'document_author_create_api'),
    path('api/author/update/create', Document_Author_Update_Create_AJAXView.as_view(), name = 'document_author_update_create_api'),
    path('api/author/create/<uuid:pk>', Document_Author_Create_Save_AJAXView.as_view(), name = 'document_author_create_save_api'),
    path('api/author/update/create/<uuid:pk>', Document_Author_Update_Create_Save_AJAXView.as_view(), name = 'document_author_update_create_save_api'),
    path('api/author/remove/<uuid:pk>', Document_Author_Remove_Save_AJAXView.as_view(), name = 'document_author_remove_save_api'),
    path('api/author/remove/update/<uuid:pk>', Document_Author_Remove_Update_Save_AJAXView.as_view(), name = 'document_author_remove_update_save_api'),
    # path('reports/print/<int:pk>', Document_Print.as_view(), name = 'document_print'),

]
