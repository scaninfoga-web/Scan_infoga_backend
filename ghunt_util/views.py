import sys
import os
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from asgiref.sync import async_to_sync

from core.utils import create_response
from .serializers import GHuntLoginSerializer, GHuntEmailInfoSerializer
from .utils import login_with_base64_creds, get_email_info

from.utils import GHuntAuthenticationError, GHuntEmailInfoError

@api_view(['POST'])
def ghunt_login(request):
    try:
        serializer = GHuntLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                create_response(
                    status=False,
                    message="Invalid input data",
                    data=serializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        success, message = async_to_sync(login_with_base64_creds)(serializer.validated_data['token'])
        
        return Response(
            create_response(
                status=success,
                message=message,
                data=None
            ),
            status=status.HTTP_200_OK if success else status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except GHuntAuthenticationError as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ),
            status=status.HTTP_401_UNAUTHORIZED
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
def email_info(request):
    try:
        serializer = GHuntEmailInfoSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                create_response(
                    status=False,
                    message="Invalid input data",
                    data=serializer.errors
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        result = async_to_sync(get_email_info)(
            serializer.validated_data['email'],
            serializer.validated_data.get('json_file')
        )
        
        return Response(
            create_response(
                status=True,
                message="Email information retrieved successfully",
                data=result
            ),
            status=status.HTTP_200_OK
        )
    except GHuntEmailInfoError as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ),
            status.HTTP_400_BAD_REQUEST
        )
    except Exception as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ),
            status.HTTP_500_INTERNAL_SERVER_ERROR
        )
