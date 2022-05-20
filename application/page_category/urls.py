from django.urls import path,include
from .import views

from .views import (
    Category_Page,
    Category_Create,
    Category_Create_AJAXView,
    Category_Update,
    Category_Update_AJAXView,
    Category_Update_Save_AJAXView,
    Category_Table_AJAXView,
    # Category_Print,
)
# 127.0.0.1:8000/category/
urlpatterns = [
    path('', Category_Page.as_view(), name = 'category'),
    path('create', Category_Create.as_view(), name = 'category_create'),
    path('api/create', Category_Create_AJAXView.as_view(), name = 'category_create_api'),
    path('update/<uuid:pk>', Category_Update.as_view(), name = 'category_update'),
    path('api/update/', Category_Update_AJAXView.as_view(), name = 'category_update_api'),
    path('api/update/save/<uuid:pk>', Category_Update_Save_AJAXView.as_view(), name = 'category_update_save_api'),
    path('api/table', Category_Table_AJAXView.as_view(), name = 'category_table_api'),
    # path('reports/print/<int:pk>', Category_Print.as_view(), name = 'category_print'),

]
