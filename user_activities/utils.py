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
        # Try to get the user from the email
        user = User.objects.get(email=email)
        
        # Convert request payload to dict if it's a string
        if isinstance(request_payload, str):
            try:
                request_payload = json.loads(request_payload)
            except json.JSONDecodeError:
                request_payload = {"raw_content": request_payload}
        
        # Ensure request_payload is a dict
        if request_payload is None:
            request_payload = {}
            
        # Create and save the activity
        activity = UserActivity.objects.create(
            user=user,
            email=email,
            api_called=api_called,
            request_payload=request_payload
        )
        return activity
    
    except User.DoesNotExist:
        # Handle case where user doesn't exist
        return None
    except Exception as e:
        # Log the error
        print(f"Error adding activity for {email}: {str(e)}")
        return None
