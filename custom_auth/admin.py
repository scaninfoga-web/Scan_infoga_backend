from django.contrib import admin
from .models import CustomUser, UserSession

admin.site.register(CustomUser)
admin.site.register(UserSession)
