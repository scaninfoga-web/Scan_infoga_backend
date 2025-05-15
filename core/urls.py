from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.decorators import api_view
from rest_framework.response import Response
from core.utils import create_response
from rest_framework import status

@api_view(['GET'])
def health_check(request):
    return Response(
            create_response(
                status=True,
                message="Backend is up and running...",
                data=None
            ),
            status=status.HTTP_200_OK
        )

urlpatterns = [
    path('health', health_check, name='health_check'),
    path('health/', health_check, name='health_check'),
    path('', health_check, name='health_check'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('custom_auth.urls')),
    path('api/ghunt/', include('ghunt_util.urls')),
    path('api/user-activities/', include('user_activities.urls')),
    path('api/mobile360/', include('mobile360.urls'))
]
