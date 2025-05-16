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


######################### UAN HISTORY ################
def fetch_uan_history_data(uan_no):
    """
    Fetch UAN history data from external API
    """
    api_url = os.getenv('UAN_HISTORY_API_URL')
    api_key = os.getenv('UAN_HISTORY_AUTH_KEY')
    
    headers = {
        'authkey': api_key,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'uan': uan_no,
        "consent": "Y",
        "consent_text": "We confirm obtaining valid customer consent to access/process their UAN data. Consent remains valid, informed, and unwithdrawn."
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        data['uan'] = uan_no
        
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


def fetch_uan_employment_data(uan_no):
    """
    Fetch UAN employment history data from external API
    """
    api_url = os.getenv('UAN_EMPLOYMENT_API_URL')
    api_key = os.getenv('UAN_EMPLOYMENT_AUTH_KEY')
    
    headers = {
        'authkey': api_key,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'uan': uan_no,
        "consent": "Y",
        "consent_text": "We confirm obtaining valid customer consent to access/process their UAN employment data. Consent remains valid, informed, and unwithdrawn."
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
        # Transform the response to match the expected format
        transformed_data = {
            'txn_id': data.get('txn_id'),
            'api_category': data.get('api_category'),
            'api_name': data.get('api_name'),
            'billable': data.get('billable'),
            'message': data.get('message'),
            'status': data.get('status'),
            'datetime': data.get('datetime'),
            'result': {
                'name': data.get('result', {}).get('name'),
                'dob': data.get('result', {}).get('dob'),
                'employment_history': data.get('result', {}).get('employment_history', [])
            }
        }
        
        return {
            'success': True,
            'data': transformed_data
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