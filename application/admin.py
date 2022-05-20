from django.contrib import admin

from .models import (
    Document_Type,
    User_Type
)


admin.site.register(Document_Type)
admin.site.register(User_Type)
