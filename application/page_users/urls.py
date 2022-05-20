from django.urls import path,include
from .import views

from .views import (
    User_Page,
    User_Create,
    User_Create_AJAXView,
    User_Update,
    User_Update_AJAXView,
    User_Update_Save_AJAXView,
    User_Table_AJAXView,
    # User_Print,
)
# 127.0.0.1:8000/user/
urlpatterns = [
    path('', User_Page.as_view(), name = 'user'),
    path('create', User_Create.as_view(), name = 'user_create'),
    path('api/create', User_Create_AJAXView.as_view(), name = 'user_create_api'),
    path('update/<uuid:pk>', User_Update.as_view(), name = 'user_update'),
    path('api/update/', User_Update_AJAXView.as_view(), name = 'user_update_api'),
    path('api/update/save/<uuid:pk>', User_Update_Save_AJAXView.as_view(), name = 'user_update_save_api'),
    path('api/table', User_Table_AJAXView.as_view(), name = 'user_table_api'),
    # path('reports/print/<int:pk>', User_Print.as_view(), name = 'user_print'),

]
