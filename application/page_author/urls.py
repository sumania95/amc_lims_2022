from django.urls import path,include
from .import views

from .views import (
    Author_Page,
    Author_Create,
    Author_Create_AJAXView,
    Author_Update,
    Author_Update_AJAXView,
    Author_Update_Save_AJAXView,
    Author_Table_AJAXView,
    # Author_Print,
)
# 127.0.0.1:8000/author/
urlpatterns = [
    path('', Author_Page.as_view(), name = 'author'),
    path('create', Author_Create.as_view(), name = 'author_create'),
    path('api/create', Author_Create_AJAXView.as_view(), name = 'author_create_api'),
    path('update/<uuid:pk>', Author_Update.as_view(), name = 'author_update'),
    path('api/update/', Author_Update_AJAXView.as_view(), name = 'author_update_api'),
    path('api/update/save/<uuid:pk>', Author_Update_Save_AJAXView.as_view(), name = 'author_update_save_api'),
    path('api/table', Author_Table_AJAXView.as_view(), name = 'author_table_api'),
    # path('reports/print/<int:pk>', Author_Print.as_view(), name = 'author_print'),

]
