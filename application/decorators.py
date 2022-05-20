from django.shortcuts import render,redirect
from django.urls import reverse
from django.contrib.auth import logout
from django.contrib.auth.mixins import AccessMixin
from .models import User_Type

class LogoutIfNotAdminMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        administrator = User_Type.objects.filter(user = self.request.user,classification=1).count()
        if administrator == 0:
            return redirect('dashboard')
        return super(LogoutIfNotAdminMixin, self).dispatch(request, *args, **kwargs)
