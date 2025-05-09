from django.urls import path
from .views import load_token, ghunt_login, extract_info_from_email

urlpatterns = [
    path('load-token', load_token, name='load-token'),
    path('ghunt-login', ghunt_login, name='ghunt-login'),
    path('extract-info-from-email', extract_info_from_email, name='extract-info-from-email'),
]