from django.urls import path
from . import views

urlpatterns = [
    path('get-user-activity', views.get_user_activity, name="get-user-activity"),
    path('get-all-user-activity', views.get_all_user_activity, name="get-all-user-activity")
]