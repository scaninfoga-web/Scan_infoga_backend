from django.urls import path
from . import views

urlpatterns = [
    path('save', views.save_hudson_data, name='save-hudson-data'),
    path('get/', views.get_hudson_data, name='get-hudson-data'),
]