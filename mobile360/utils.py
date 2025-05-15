import requests
import os
import json

def fetch_mobile360_data(mobile_number):
    """
    Fetch mobile360 data from external API
    """
    api_url = os.getenv('MOBILE360_API_URL')
    api_key = os.getenv('MOBILE360_AUTH_KEY')
    
    headers = {
        'authkey': api_key,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'mobile': mobile_number,
        "consent" : "Y",
        "consent_text" : "We confirm obtaining valid customer consent to access/process their mobile data. Consent remains valid, informed, and unwithdrawn."
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise exception for non-200 status codes
        
        # Parse the response
        data = response.json()
        
        # Add mobile number to the response for consistency
        data['mobile_number'] = mobile_number
        
        return {
            'success': True,
            'data': data
        }
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f"API request failed: {str(e)}"
        }
    except json.JSONDecodeError:
        return {
            'success': False,
            'error': "Failed to parse API response"
        }
    except Exception as e:
        return {
            'success': False,
            'error': f"Unexpected error: {str(e)}"
        }