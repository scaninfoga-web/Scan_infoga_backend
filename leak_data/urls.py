from django.urls import path
from . import views

urlpatterns = [
    # path('get-password', views.get_passwords, name='get-passwords'),
    path('get-password', views.GetPassword.as_view(), name='get-passwords'),
    path('get-jobseeker', views.GetJobSeekerData.as_view(), name='get-jobseeker-data'),

]