import os
import json
import asyncio
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import TokenUpdationLog
from core.utils import create_response
import httpx
from ghunt.modules.login import check_and_login
from ghunt.modules.email import hunt
# from drf_yasg.utils import swagger_auto_schema
# from .serializers import TokenSerializer, TokenUpdationLogSerializer

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def load_token(request):
    try:
        token_payload = request.data.get('token')
        if not token_payload:
            return Response(
                create_response(
                    status=False,
                    message='Token payload is required',
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create secrets directory if it doesn't exist
        secrets_dir = os.path.join(settings.BASE_DIR, 'secrets')
        os.makedirs(secrets_dir, exist_ok=True)
        
        # Write token to ghunt_creds.m file
        creds_file = os.path.join(secrets_dir, 'ghunt_creds.m')
        with open(creds_file, 'w') as f:
            json.dump(token_payload, f)
        
        # Log the token update
        TokenUpdationLog.objects.create(user=request.user)
        
        return Response(
            create_response(
                status=True,
                message='Token updated successfully',
                data=None
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
def ghunt_login(request):
    try:
        
        # Create an event loop in the current thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        async def run_login():
            async with httpx.AsyncClient() as client:
                await check_and_login(client, False)
        
        # Run the async function
        loop.run_until_complete(run_login())
        loop.close()
        
        return Response(
            create_response(
                status=True,
                message='Login successful',
                data=None
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
def extract_info_from_email(request):
    email = request.data.get('email')
    if not email:
        return Response(
            create_response(
                status=False,
                message='Email is required',
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    try:
        # Create an event loop in the current thread
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        async def run_hunt():
            async with httpx.AsyncClient() as client:
                result = await hunt(client, email, False)
                return result
        # Run the async function
        result = loop.run_until_complete(run_hunt())
        loop.close()
        return Response(
            create_response(
                status=True,
                message='Info extracted successfully',
                data=result
            ),
            status=status.HTTP_200_OK
        )
    except Exception as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None   
            )
        )