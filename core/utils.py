import jwt
from django.conf import settings

def create_response(status, message, data = None):
    return {
        "responseStatus": {
            "status": status,
            "message": message
        },
        "responseData": data
    }

def get_token_from_header(request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        token = auth_header.split(' ')[1]
        return token
    return None
    
def get_email_from_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    email = payload.get("email")
    return email

def create_token(user):
    payload = {
        "email": user.email,
        "user_type": user.user_type
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def get_user_from_token(token):
    payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
    email = payload.get("email")
    user_type = payload.get("user_type")
    user = CustomUser.objects.get(email=email, user_type=user_type)
    return user