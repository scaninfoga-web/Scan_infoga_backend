from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
import pyotp
import qrcode
import base64
from io import BytesIO
from .serializers import UserRegistrationSerializer, CorporateRegistrationSerializer, DeveloperRegistrationSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
import hashlib
from .models import UserSession, CustomUser
from user_agents import parse
from django.utils import timezone
from core.utils import create_response
from google.oauth2 import id_token
from google.auth.transport import requests
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from rest_framework.decorators import parser_classes
from django.http import HttpResponse

from .utils import fetch_map
from payments.utils import create_wallet

@api_view(['POST'])
def registerUser(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        # Generate secret key and QR code after user is created
        secret_key = pyotp.random_base32()
        user.otp_secret = secret_key
        user.save()

        # create wallet for user after user is created 
        # and by default add 2000 credit
        create_wallet(user)
        
        # Generate QR code
        qr_code = generate_qr_code(user.email, secret_key)
        
        response_data = serializer.data
        response_data['qr_code'] = qr_code
        
        return Response(
            create_response(
                status=True,
                message="User registered successfully. Please scan the QR code to setup 2FA.",
                data=response_data
            ),
            status=status.HTTP_201_CREATED
        )
    return Response(
        create_response(
            status=False,
            message="Registration failed",
            data=serializer.errors
        ),
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
def loginUser(request):
    email = request.data.get('email')
    password = request.data.get('password')
    otp = request.data.get('otp')
    userType = request.data.get('userType')
    
    # First step: Email and password authentication
    if not all([email, password, userType]):
        return Response(
            create_response(
                status=False,
                message="Please provide email, password and user type",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

    if userType not in ['crp', 'dev', 'user']:
        return Response(
            create_response(
                status=False,
                message="Invalid user type",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

    hashedPassword = hashlib.sha256(password.encode()).hexdigest()
    user = authenticate(email=email, password=hashedPassword)

    if not user:
        return Response(
            create_response(
                status=False,
                message="Invalid credentials",
                data=None
            ),
            status=status.HTTP_401_UNAUTHORIZED
        )
        
    user_type_map = {
        'crp': 'CORPORATE',
        'dev': 'DEVELOPER',
        'user': 'USER'
    }
    
    if user.user_type != user_type_map.get(userType):
        return Response(
            create_response(
                status=False,
                message=f"Invalid login. Please use {user.user_type.lower()} login",
                data=None
            ),
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Second step: Request OTP
    if not otp:
        return Response(
            create_response(
                status=True,
                message="Please provide OTP",
                data={'require_otp': True}
            ),
            status=status.HTTP_200_OK
        )

    # Third step: Verify OTP and generate token
    totp = pyotp.TOTP(user.otp_secret)
    if not totp.verify(otp):
        return Response(
            create_response(
                status=False,
                message="Invalid OTP",
                data=None
            ),
            status=status.HTTP_401_UNAUTHORIZED
        )

    # Generate token and complete login
    from core.utils import create_token
    # token = create_token(user)
    refresh = RefreshToken.for_user(user)
    token = str(refresh.access_token)

    user_data = {
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'userType': user.user_type
    }

    return Response(
        create_response(
            status=True,
            message="Login successful",
            data={'user': user_data, 'accessToken': token}
        ),
        status=status.HTTP_200_OK
    )

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protectedApi(request):
    return Response(
        create_response(
            status=True,
            message="Access granted to protected API",
            data={
                'user': {
                    'email': request.user.email,
                    'firstName': request.user.first_name,
                    'lastName': request.user.last_name
                }
            }
        )
    )

@api_view(['POST'])
def googleAuth(request):
    try:
        idToken = request.data.get('idToken')
        backend = request.data.get('backend')
        grant_type = request.data.get('grant_type')

        if not all([idToken, backend, grant_type]):
            return Response(
                create_response(
                    status=False,
                    message="ID token, backend, and grant_type are required",
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        if backend != 'google-oauth2' or grant_type != 'convert_token':
            return Response(
                create_response(
                    status=False,
                    message="Invalid backend or grant_type",
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verify Google token
        idInfo = id_token.verify_oauth2_token(
            idToken,
            requests.Request(),
            settings.GOOGLE_OAUTH_CLIENT_ID
        )

        # Additional verification
        if idInfo['aud'] != settings.GOOGLE_OAUTH_CLIENT_ID:
            raise ValueError('Invalid audience')
        if idInfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError('Invalid issuer')

        email = idInfo['email']
        firstName = idInfo.get('given_name', '')
        lastName = idInfo.get('family_name', '')

        # Check if user exists or create new one
        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                'first_name': firstName,
                'last_name': lastName,
            }
        )

        # Generate JWT token
        refresh = RefreshToken.for_user(user)

        # Create user session
        userAgentString = request.META.get('HTTP_USER_AGENT', '')
        userAgent = parse(userAgentString)
        
        UserSession.objects.create(
            email=user,
            ipAddress=request.META.get('REMOTE_ADDR', ''),
            device=f"{userAgent.device.family} {userAgent.device.model}",
            browser=f"{userAgent.browser.family} {userAgent.browser.version_string}",
            location=request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', '')),
            sessionStartTime=timezone.now()
        )

        return Response(
            create_response(
                status=True,
                message="Google authentication successful",
                data={
                    'user': {
                        'email': user.email,
                        'firstName': user.first_name,
                        'lastName': user.last_name,
                        'isNewUser': created
                    },
                    'accessToken': str(refresh.access_token)
                }
            ),
            status=status.HTTP_200_OK
        )


    except ValueError as e:
        return Response(
            create_response(
                status=False,
                message="Invalid Google token",
                data=str(e)
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

@api_view(['POST'])
def registerDeveloper(request):
    serializer = DeveloperRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        developer = serializer.save()
        return Response(
            create_response(
                status=True,
                message="Developer registered successfully",
                data={
                    'email': developer.user.email,
                    'firstName': developer.first_name,
                    'lastName': developer.last_name
                }
            ),
            status=status.HTTP_201_CREATED
        )
    return Response(
        create_response(
            status=False,
            message="Registration failed",
            data=serializer.errors
        ),
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(['POST'])
def registerCorporate(request):
    serializer = CorporateRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        corporate = serializer.save()
        return Response(
            create_response(
                status=True,
                message="Corporate registration submitted for approval",
                data={
                    'email': corporate.user.email,
                    'firstName': corporate.first_name,
                    'lastName': corporate.last_name,
                    'company': corporate.company,
                    'domain': corporate.domain,
                    'approvalStatus': corporate.approval_status
                }
            ),
            status=status.HTTP_201_CREATED
        )
    return Response(
        create_response(
            status=False,
            message="Registration failed",
            data=serializer.errors
        ),
        status=status.HTTP_400_BAD_REQUEST
    )

    if CustomUser.objects.filter(email=email).exists():
        return Response(
            create_response(
                status=False,
                message="This email is already registered. Please use a different email.",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )

def generate_qr_code(email, secret_key):
    totp = pyotp.TOTP(secret_key)
    provisioning_uri = totp.provisioning_uri(email, issuer_name="YourApp")
    
    # Generate QR code
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(provisioning_uri)
    qr.make(fit=True)
    
    # Create QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    qr_code = base64.b64encode(buffer.getvalue()).decode()
    
    return qr_code

@api_view(['POST'])
@parser_classes([JSONParser, FormParser, MultiPartParser])
def get_user_map(request):
    # Get user's location
    user_location_lng = request.data.get('userLng')
    user_location_lat = request.data.get('userLat')
    address = request.data.get('address')
    
    if not all([user_location_lat, user_location_lng, address]):
        return Response(
            create_response(
                status=False,
                message="Please provide user's location and address location",
                data=None
            ),
            status=status.HTTP_400_BAD_REQUEST
        )
    
    try:
        api_response = fetch_map(
            starting_point_lng=user_location_lng, 
            starting_point_lat=user_location_lat, 
            address=address
        )
        
        # Option 1: Return base64 encoded image in JSON response
        return Response(
            create_response(
                status=api_response['success'],
                message="Map fetched successfully",
                data=api_response['data']
            ),
            status=status.HTTP_200_OK
        )
        
        # Option 2: Return image directly
        # image_data = base64.b64decode(api_response['data']['image'])
        # return HttpResponse(
        #     image_data,
        #     content_type=api_response.get('content_type', 'image/png')
        # )
    
    except Exception as e:
        return Response(
            create_response(
                status=False,
                message="Error fetching map",
                data=str(e)
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )