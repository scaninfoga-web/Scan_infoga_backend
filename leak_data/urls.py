from django.urls import path
from . import views

urlpatterns = [
    path('get-password', views.get_passwords, name='get-passwords'),
]