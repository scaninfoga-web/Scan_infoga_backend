from django.urls import path
from . import views

urlpatterns = [
    path('all/', views.get_all_user_activity, name='get-all-user-activity'),
    path('by-email/', views.get_user_activity_by_email, name='get-user-activity-by-email'),
    path('add/', views.add_user_activity, name='add-user-activity'),
]