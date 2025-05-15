from django.urls import path
from . import views

urlpatterns = [
    path('login', views.ghunt_login, name='ghunt-login'),
    path('getEmailDetails', views.email_info, name='ghunt-email-info'),
]