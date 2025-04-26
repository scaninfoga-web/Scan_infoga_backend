from django.urls import path
from . import views

urlpatterns = [
    path('register', views.registerUser, name='register'),
    path('register/developer', views.registerDeveloper, name='register-developer'),
    path('register/corporate', views.registerCorporate, name='register-corporate'),
    path('login', views.loginUser, name='login'),
    path('google/', views.googleAuth, name='login'),
    path('protected/', views.protectedApi, name='protected'),
]