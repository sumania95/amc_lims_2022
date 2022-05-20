from django.urls import path,include
from .import views

from .views import (
    Login,
    Logout,
)

urlpatterns = [
    path('login', Login.as_view(), name = 'login'),
    path('logout', Logout.as_view(), name = 'logout'),
]
