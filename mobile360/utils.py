import requests
import os
import json
from datetime import datetime  # Add this import
from dotenv import load_dotenv
from .transform import transform_api_response, prepare_client_response

load_dotenv()


def fetch_mobile360_data(mobile_number):
    """Fetch mobile360 data from external API"""
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
        response.raise_for_status()
        
        # Parse and transform the response
        data = response.json()
        transformed_data = transform_api_response(data, mobile_number)
        client_response = prepare_client_response(transformed_data)
        
        return {
            'success': True,
            'data': client_response
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
    api_key = os.getenv('UAN_AUTH_KEY')
    
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
        
        # Transform and validate the response with datetime handling
        current_time = datetime.now().isoformat()
        transformed_data = {
            'txn_id': data.get('txn_id'),
            'api_category': data.get('api_category'),
            'api_name': data.get('api_name'),
            'billable': data.get('billable', False),
            'message': data.get('message', ''),
            'status': data.get('status', 0),
            'datetime': data.get('datetime', current_time),
            'result': {
                'name': data.get('result', {}).get('name', 'Unknown'),
                'dob': data.get('result', {}).get('dob', '1900-01-01'),
                'guardian_name': data.get('result', {}).get('guardian_name', 'Unknown'),
                'company_name': data.get('result', {}).get('company_name', 'Unknown'),
                'member_id': data.get('result', {}).get('member_id', ''),
                'date_of_joining': data.get('result', {}).get('date_of_joining', '1900-01-01'),
                'last_pf_submitted': data.get('result', {}).get('last_pf_submitted', '1900-01-01')
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


def fetch_uan_employment_data(uan_no):
    """
    Fetch UAN employment history data from external API
    """
    api_url = os.getenv('UAN_EMPLOYMENT_API_URL')
    api_key = os.getenv('UAN_AUTH_KEY')
    
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
        
        # Transform the response to match the expected format with default values
        transformed_data = {
            'txn_id': data.get('txn_id'),
            'api_category': data.get('api_category'),
            'api_name': data.get('api_name'),
            'billable': data.get('billable'),
            'message': data.get('message'),
            'status': data.get('status'),
            'datetime': data.get('datetime'),
            'result': {
                'name': data.get('result', {}).get('name') or 'Unknown',  # Default value if null
                'dob': data.get('result', {}).get('dob') or '01/01/1900',  # Default value if null
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
        
##################### ESIC ##################
def fetch_esic_data(mobile_number):
    """
    Fetch ESIC details data from external API
    """
    api_url = os.getenv('ESIC_API_URL')
    api_key = os.getenv('ESIC_AUTH_KEY')
    
    headers = {
        'authkey': api_key,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'esic_number': mobile_number,
        "consent": "Y",
        "consent_text": "We confirm obtaining valid customer consent to access/process their esic data. Consent remains valid, informed, and unwithdrawn."
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
            'result': data.get('result', [])
        }
        print("TD")
        print(transformed_data)  # Add this line for debugging
        
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

##################### GST Advance ##################
def fetch_gst_data(gstin):
    """
    Fetch GST verification data from external API
    """
    api_url = os.getenv('GST_API_URL')
    api_key = os.getenv('GST_AUTH_KEY')
    
    headers = {
        'authkey': api_key,
        'Content-Type': 'application/json'
    }
    
    payload = {
        'gstin': gstin,
        "consent": "Y",
        "consent_text": "We confirm that we have obtained the consent of the respective customer to fetch their details from authorized sources using their GST"
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        data = response.json()
        
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
        
##################### GST Turnover ##################
def fetch_gst_turnover_data(gstin, year):
    """
    Fetch GST turnover data from external API.
    """
    api_url = os.getenv('GST_TURNOVER_API_URL')
    api_key = os.getenv('GST_AUTH_KEY')

    headers = {
        'authkey': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'gstin': gstin,
        'year': year,
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()

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