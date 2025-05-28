import json
import jwt
from django.conf import settings
from django.utils.timezone import now
from custom_auth.models import CustomUser as User
from django.http import JsonResponse
from rest_framework import status
from user_activities.models import UserActivity
from .utils import create_response

class GlobalExceptionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.log_user_activity(request)
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        return JsonResponse(
            create_response(
                status=False,
                message=str(exception),
                data=None
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    def log_user_activity(self, request):
        try:
            # 1. Decode JWT Token
            auth_header = request.headers.get("Authorization", "")
            token = auth_header.split(" ")[1] if auth_header.startswith("Bearer ") else None
            email = None
            user = None

            if token:
                payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                email = payload.get("email")  # Adjust key if needed (e.g., 'email')
                if email:
                    user = User.objects.filter(email=email).first()

            # 2. Parse clientInfo
            client_info_raw = request.headers.get("clientInfo", "{}")

            try:
                client_info = json.loads(client_info_raw)
            except json.JSONDecodeError as e:
                client_info = {}

            # 3. Parse payload
            try:
                payload_data = json.loads(request.body.decode('utf-8')) if request.body else {}
            except Exception:
                payload_data = {}

            # 4. Save to DB
            if user:
                UserActivity.objects.create(
                    user=user,
                    email=user.email,
                    api_called=request.path,
                    request_payload=payload_data,
                    ip_address=client_info.get("ipAddress", request.META.get("REMOTE_ADDR", "")),
                    device=client_info.get("device", ""),
                    browser=client_info.get("browser", ""),
                    latitude=client_info.get("latitude", ""),
                    longitude=client_info.get("longitude", "")
                )

                print("Created user activity")
            else:
                print("User not found did not create")
        except Exception as e:
            # Don't break request flow if activity logging fails
            print("Exception from middleware log user activity: ", str(e))
            pass
