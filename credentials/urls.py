from django.urls import path
from .views import GetPasswordView

urlpatterns = [
    path('get-password/', GetPasswordView.as_view()),
]
