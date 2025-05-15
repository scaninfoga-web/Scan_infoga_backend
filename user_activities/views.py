from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import UserActivity
from .serializers import UserActivitySerializer
from .utils import add_activity
from core.utils import create_response

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_user_activity(request):
    """
    API endpoint to get all user activities
    """
    try:
        activities = UserActivity.objects.all()
        serializer = UserActivitySerializer(activities, many=True)
        
        return Response(
            create_response(
                status=True,
                message="User activities retrieved successfully",
                data=serializer.data
            ),
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_activity_by_email(request):
    """
    API endpoint to get activities for a specific user by email
    """
    try:
        email = request.GET.get('email')
        
        if not email:
            return Response(
                create_response(
                    status=False,
                    message="Email parameter is required",
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        activities = UserActivity.objects.filter(email=email)
        serializer = UserActivitySerializer(activities, many=True)
        
        return Response(
            create_response(
                status=True,
                message="User activities retrieved successfully",
                data=serializer.data
            ),
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_user_activity(request):
    try:
        data = request.data
        email = data.get('email')
        api_called = data.get('api_called')
        request_payload = data.get('request_payload', {})
        
        if not email or not api_called:
            return Response(
                create_response(
                    status=False,
                    message="Email and api_called fields are required",
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Use the utility function to add the activity
        activity = add_activity(email, api_called, request_payload)
        
        if activity:
            serializer = UserActivitySerializer(activity)
            return Response(
                create_response(
                    status=True,
                    message="Activity added successfully",
                    data=serializer.data
                ),
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                create_response(
                    status=False,
                    message="Failed to add activity. User may not exist.",
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
    
    except Exception as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )