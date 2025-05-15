from django.contrib.auth import get_user_model
from .models import UserActivity
import json

User = get_user_model()

def add_activity(email, api_called, request_payload=None):
    """
    Utility function to add a new user activity record
    
    Args:
        email (str): User's email
        api_called (str): Name of the API that was called
        request_payload (dict, optional): The payload sent with the request
    
    Returns:
        UserActivity: The created UserActivity instance
    """
    try:
        user = User.objects.get(email=email)
        
        if isinstance(request_payload, str):
            try:
                request_payload = json.loads(request_payload)
            except json.JSONDecodeError:
                request_payload = {"raw_content": request_payload}
        
        if request_payload is None:
            request_payload = {}
            
        activity = UserActivity.objects.create(
            user=user,
            email=email,
            api_called=api_called,
            request_payload=request_payload
        )
        return activity
    
    except User.DoesNotExist:
        return None
    except Exception as e:
        print(f"Error adding activity for {email}: {str(e)}")
        return None
