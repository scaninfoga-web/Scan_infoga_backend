from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registerUser, name='register'),
    path('change-password', views.changePassword, name='change-password'),
    path('change-email', views.changeEmail, name='change-email'),
    path('register/developer', views.registerDeveloper, name='register-developer'),
    path('register/corporate', views.registerCorporate, name='register-corporate'),
    path('login', views.loginUser, name='login'),
    path('google/', views.googleAuth, name='login'),
    path('protected', views.protectedApi, name='protected'),
    path('getmap', views.get_user_map, name='get-map'),
]