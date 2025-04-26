from django.urls import path, include

urlpatterns = [
    # ... existing code ...
    path('api/hudson/', include('hudsonrock.urls')),
]