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

@api_view(['POST'])
def registerUser(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            create_response(
                status=True,
                message="User registered successfully",
                data=serializer.data
            ),
            status=status.HTTP_201_CREATED
        )
    return Response(
        create_response(
            status=False,
            message="Registration failed",
            data=serializer.errors  #"user exists" if "email" in serializer.errors.keys else serializer.errors
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
def loginUser(request):
    email = request.data.get('email')
    password = request.data.get('password')
    otp = request.data.get('otp')
    userType = request.data.get('userType')
    
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

    # If OTP is not provided, generate and return QR code
    if not otp:
        # Generate or get existing secret key for user
        if not hasattr(user, 'otp_secret'):
            secret_key = pyotp.random_base32()
            user.otp_secret = secret_key
            user.save()
        else:
            secret_key = user.otp_secret
            
        # Generate QR code
        qr_code = generate_qr_code(user.email, secret_key)
        
        return Response(
            create_response(
                status=True,
                message="Please scan QR code and provide OTP",
                data={'qr_code': qr_code}
            ),
            status=status.HTTP_200_OK
        )

    # Verify OTP
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

    # Continue with existing login logic after OTP verification
    if user.user_type == 'CORPORATE':
        corporate_profile = user.corporate_profile
        if corporate_profile.approval_status != 'APPROVED':
            return Response(
                create_response(
                    status=False,
                    message="Your corporate account is pending approval",
                    data={'approvalStatus': corporate_profile.approval_status}
                ),
                status=status.HTTP_401_UNAUTHORIZED
            )

    refresh = RefreshToken.for_user(user)
    
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
    
    user_data = {
        'email': user.email,
        'firstName': user.first_name,
        'lastName': user.last_name,
        'userType': user.user_type
    }

    if user.user_type == 'CORPORATE':
        user_data.update({
            'company': user.corporate_profile.company,
            'domain': user.corporate_profile.domain,
            'approvalStatus': user.corporate_profile.approval_status
        })
    
    return Response(
        create_response(
            status=True,
            message="Login successful",
            data={
                'user': user_data,
                'accessToken': str(refresh.access_token)
            }
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
