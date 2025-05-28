from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserActivity
from .serializers import UserActivitySerializer
from .utils import add_activity
from core.utils import create_response, get_token_from_header, get_email_from_token 

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_activity(request):
    token = get_token_from_header(request)
    email = get_email_from_token(token)
    activities = UserActivity.objects.filter(email=email, api_called="/api/mobile/getMobile360Dtls")
    serializer = UserActivitySerializer(activities, many=True)
    return Response(
            create_response(
                status=True,
                message="User activities retrieved successfully",
                data=serializer.data
            ),
            status=status.HTTP_200_OK
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def get_all_user_activity(request): #request
    activities = UserActivity.objects.filter(api_called="/api/mobile/getMobile360Dtls")
    serializer = UserActivitySerializer(activities, many=True)
    return Response(
            create_response(
                status=True,
                message="User activities retrieved successfully",
                data=serializer.data
            ),
    )