from django.urls import path,include
from .import views

from .views import (
    Year_Term_Page,
    Year_Term_Create,
    Year_Term_Create_AJAXView,
    Year_Term_Update,
    Year_Term_Update_AJAXView,
    Year_Term_Update_Save_AJAXView,
    Year_Term_Table_AJAXView,
    # Year_Term_Print,
)
# 127.0.0.1:8000/year/
urlpatterns = [
    path('', Year_Term_Page.as_view(), name = 'year'),
    path('create', Year_Term_Create.as_view(), name = 'year_create'),
    path('api/create', Year_Term_Create_AJAXView.as_view(), name = 'year_create_api'),
    path('update/<uuid:pk>', Year_Term_Update.as_view(), name = 'year_update'),
    path('api/update/', Year_Term_Update_AJAXView.as_view(), name = 'year_update_api'),
    path('api/update/save/<uuid:pk>', Year_Term_Update_Save_AJAXView.as_view(), name = 'year_update_save_api'),
    path('api/table', Year_Term_Table_AJAXView.as_view(), name = 'year_table_api'),
    # path('reports/print/<int:pk>', Year_Term_Print.as_view(), name = 'year_print'),

]
