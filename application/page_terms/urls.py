from django.urls import path,include
from .import views

from .views import (
    Terms_Page,
    Terms_Create,
    Terms_Create_AJAXView,
    Terms_Update,
    Terms_Update_AJAXView,
    Terms_Update_Save_AJAXView,
    Terms_Table_AJAXView,
    Terms_Author_Table_AJAXView,
    Terms_Author_Update_Table_AJAXView,
    Terms_Author_View_Table_AJAXView,
    Terms_Author_Update_View_Table_AJAXView,
    Terms_Author_Create_AJAXView,
    Terms_Author_Update_Create_AJAXView,
    Terms_Author_Create_Save_AJAXView,
    Terms_Author_Update_Create_Save_AJAXView,
    Terms_Author_Remove_Save_AJAXView,
    Terms_Author_Remove_Update_Save_AJAXView
    # Terms_Print,
)
# 127.0.0.1:8000/terms/
urlpatterns = [
    path('', Terms_Page.as_view(), name = 'terms'),
    path('create', Terms_Create.as_view(), name = 'terms_create'),
    path('api/create', Terms_Create_AJAXView.as_view(), name = 'terms_create_api'),
    path('update/<uuid:pk>', Terms_Update.as_view(), name = 'terms_update'),
    path('api/update/', Terms_Update_AJAXView.as_view(), name = 'terms_update_api'),
    path('api/update/save/<uuid:pk>', Terms_Update_Save_AJAXView.as_view(), name = 'terms_update_save_api'),
    path('api/table', Terms_Table_AJAXView.as_view(), name = 'terms_table_api'),
    path('api/author/table', Terms_Author_Table_AJAXView.as_view(), name = 'terms_author_table_api'),
    path('api/author/table/update', Terms_Author_Update_Table_AJAXView.as_view(), name = 'terms_author_update_table_api'),
    path('api/author/table/view', Terms_Author_View_Table_AJAXView.as_view(), name = 'terms_author_view_table_api'),
    path('api/author/table/update/view', Terms_Author_Update_View_Table_AJAXView.as_view(), name = 'terms_author_update_view_table_api'),
    path('api/author/create', Terms_Author_Create_AJAXView.as_view(), name = 'terms_author_create_api'),
    path('api/author/update/create', Terms_Author_Update_Create_AJAXView.as_view(), name = 'terms_author_update_create_api'),
    path('api/author/create/<uuid:pk>', Terms_Author_Create_Save_AJAXView.as_view(), name = 'terms_author_create_save_api'),
    path('api/author/update/create/<uuid:pk>', Terms_Author_Update_Create_Save_AJAXView.as_view(), name = 'terms_author_update_create_save_api'),
    path('api/author/remove/<uuid:pk>', Terms_Author_Remove_Save_AJAXView.as_view(), name = 'terms_author_remove_save_api'),
    path('api/author/remove/update/<uuid:pk>', Terms_Author_Remove_Update_Save_AJAXView.as_view(), name = 'terms_author_remove_update_save_api'),
    # path('reports/print/<int:pk>', Terms_Print.as_view(), name = 'terms_print'),

]
