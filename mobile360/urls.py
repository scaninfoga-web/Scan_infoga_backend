from django.urls import path
from . import views

app_name = 'mobile360'

urlpatterns = [
    path('/getMobile360Dtls', views.mobile_360_search, name='mobile_360_search'),
]