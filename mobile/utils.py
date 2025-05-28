import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from urllib3.poolmanager import key_fn_by_scheme
from .transform import transform_api_response, prepare_client_response
import asyncio
import aiohttp

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
    
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    if response.json()['status'] == 1:
        data = response.json()
        transformed_data = transform_api_response(data, mobile_number)
        client_response = prepare_client_response(transformed_data)
        return {
            'success': True,
            'data': client_response
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')

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
        
        return {
            'success': True if (data.get('status') == 1 or data.get('status') == 2) else False,
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

################### UAN Employment History ###################
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
    
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    
    data = response.json()
    if data['status'] == 1:
        return {
            'success': True,
            'data': data
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')
    

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
        'gst_no': gstin,
        "consent": "Y",
        "consent_text": "We confirm that we have obtained the consent of the respective customer to fetch their details from authorized sources using their GST"
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()
    
    data = response.json()
    if data['status'] == 1:
        return {
            'success': True,
            'data': data
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')

        
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
        'gst_no': gstin,
        'year': year,
    }

    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    if data['status']==1:
        return {
            'success': True,
            'data': data
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')
        
################### Verify Udyam ###################
def fetch_udyam_data(udyam_number):
    """
    Fetch Udyam data from external API
    """
    api_url = os.getenv('UDYAM_API_URL')
    api_key = os.getenv('UDYAM_AUTH_KEY')

    headers = {
        'authkey': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'registration_no': udyam_number,
    }

    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    if data['status']==1:
        return {
            'success': True,
            'data': data
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')


################### Mobile to Account ###################
def fetch_mobile_to_account_data(mobile_number):
    """
    Fetch Mobile to Account data from external API
    """
    api_url = os.getenv('MOBILE_TO_ACCOUNT_API_URL')
    api_key = os.getenv('MOBILE_TO_ACCOUNT_AUTH_KEY')

    headers = {
        'authkey': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'mobile': mobile_number,
        "consent" :"Y",
        "consent_text":"We confirm obtaining valid customer consent to access/process their mobile data. Consent remains valid, informed, and unwithdrawn."
    }

    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    if data['status']==1:
        return {
            'success': True,
            'data': data
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')

################### Profile Advance ###################
def fetch_profile_advance_data(mobile_number):
    """
    Fetch Profile Advance data from external API
    """
    api_url = os.getenv('PROFILE_ADVANCE_API_URL')
    api_key = os.getenv('PROFILE_ADVANCE_AUTH_KEY')
    
    headers = {
        "authkey": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        'mobile':mobile_number,
        "consent": "Y",
        "consent_text": "We confirm obtaining valid customer consent to access/process their mobile data. Consent remains valid, informed, and unwithdrawn."
    }
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    if data['status']==1:
        return {
            'success': True,
            'data': data
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')

################### Equifax V3 ###################
def fetch_equifax_data(id_number, id_type, mobile_number, name):
    """
    Fetch Equifax V3 data from external API
    """
    api_url = os.getenv('EQUIFAX_API_URL')
    api_key = os.getenv('EQUIFAX_AUTH_KEY')
    
    headers = {
        "authkey": api_key,
        "Content-Type": "application/json"
    }
    
    payload = {
        "mobile": mobile_number,
        "name": name,
        'docNumber': id_number,
        'docType': id_type,
        "consent": "Y",
        "consent_text": "We confirm obtaining valid customer consent to access/process their mobile and PAN/Aadhaar data. Consent remains valid, informed, and unwithdrawn."
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    if data['status']==1:
        return {
            'success': True,
            'data': data
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')

################# mobile to account ##########
def fetch_mobile_to_account_data(mobile_number):
    """
    Fetch Mobile to Account data from external API
    """
    api_url = os.getenv('MOBILE_TO_ACCOUNT_API_URL')
    api_key = os.getenv('MOBILE_TO_ACCOUNT_AUTH_KEY')

    headers = {
        "authkey": api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "mobile": mobile_number,
        "consent": "Y",
        "consent_text": "We confirm obtaining valid customer consent to access/process their mobile data. Consent remains valid, informed, and unwithdrawn."
    }
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    if data['status']==1:
        return {
            'success': True,
            'data': data
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')

def get_uan_dtls_without_otp(uan_no):
    """
    Fetch UAN passbook details without OTP from external API using a two-step process:
    1. Get request_id from first API endpoint
    2. Use request_id to get full details from second API endpoint
    """
    # Step 1: Get request_id
    request_id_url = os.getenv('UAN_WITHOUT_OTP_REQ_URL')
    details_url = os.getenv('UAN_WITHOUT_OTP_DTL_URL')
    api_key = os.getenv('UAN_WITHOUT_OTP_AUTH_KEY')
    
    headers = {
        'authkey': api_key,
        'Content-Type': 'application/json'
    }
    
    # First API call to get request_id
    request_id_payload = {
        'uan': uan_no
    }
    
    try:
        # Step 1: Get request_id
        request_id_response = requests.post(request_id_url, headers=headers, json=request_id_payload)
        request_id_response.raise_for_status()
        
        request_id_data = request_id_response.json()
        
        if not request_id_data.get('status') == 1 or 'result' not in request_id_data or 'request_id' not in request_id_data['result']:
            return {
                'success': False,
                'error': f"Failed to get request_id: {request_id_data.get('message', 'Unknown error')}"
            }
        
        request_id = request_id_data['result']['request_id']
        
        # Step 2: Get details using request_id
        details_payload = {
            'request_id': request_id,
            'consent': 'Y',
            'consent_text': 'We confirm obtaining valid customer consent to access/process their UAN data. Consent remains valid, informed, and unwithdrawn.'
        }
        
        details_response = requests.post(details_url, headers=headers, json=details_payload)
        details_response.raise_for_status()
        
        details_data = details_response.json()
        
        return {
            'success': True,
            'data': details_data
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

def fetch_mobile_to_dl_data(mobile_number, name, dob):
    """
    Fetch driving license details from mobile number using external API
    
    Args:
        mobile_number (str): Mobile number to search
        
    Returns:
        dict: API response with success flag and data
    """
    api_url = os.getenv('MOBILE_TO_DL_API_URL')
    api_key = os.getenv('MOBILE_TO_DL_AUTH_KEY')
    
    payload = {
        "mobile_number": mobile_number,
        "name": name,
        "dob": dob
    }

    headers = {
    'authkey': api_key,
    'Content-Type': 'application/json'
    }

    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    if data['status']==1:
        return {
            'success': True,
            'data': data
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')
        

def fetch_pan_all_in_one_data(pan_number):
    """
    Fetch PAN details from external API
    """
    api_url = os.getenv('PAN_ALL_IN_ONE_API_URL')
    api_key = os.getenv('PAN_ALL_IN_ONE_AUTH_KEY')

    headers = {
        'authkey': api_key,
        'Content-Type': 'application/json'
    }

    payload = {
        'pan': pan_number,
    }
    
    response = requests.post(api_url, headers=headers, json=payload)
    response.raise_for_status()

    data = response.json()
    if data['status']==1:
        return {
            'success': True,
            'data': data
        }
    raise Exception(response.json()['message'] or 'Unexpected Error')


upi_handles = {
    # App UPI Handles
    'PhonePe': ['@ybl', '@ibl', '@axl'],
    # 'Google Pay': ['@okhdfcbank', '@okaxis', '@okicici'],
    'Paytm': ['@paytm', '@ptyes'],
    'Amazon Pay': ['@apl', '@yapl', '@rapl', '@amazonpay'],
    'BHIM': ['@upi'],
    'CRED': ['@yescred'],
    'Groww': ['@yesg'],
    'Mobikwik': ['@ikwik', '@mbk'],
    'Jupiter': ['@jupiteraxis'],
    'Slice': ['@sliceaxis'],
    'Tata Neu': ['@tapicici'],
    'Zomato': ['@zoicici'],
    'Fampay': ['@fam'],
    'OkCredit': ['@axb'],
    'MyJio UPI': ['@jio'],
    'PayZapp': ['@pz'],
    'Spice Money': ['@spicepay'],
    'OneCard': ['@oneyes'],
    'POPclub': ['@yespop'],
    'SalarySe': ['@seyes'],
    'super.money': ['@superyes'],
    'FamApp by Trio': ['@yesfam'],
    'ICICI Pockets App': ['@pockets'],
    'Fi Money (Federal Bank)': ['@fifederal'],
    'Bajaj Finserv': ['@abfspay'],
    'WhatsApp': ['@waicici', '@wahdfcbank', '@waaxis', '@wasbi'],
    'OmniCard': ['@omni'],
    'Dhani': ['@dhani'],
    'Cheq': ['@trans'],
    'QuikWallet': ['@liv'],
    'NYE': ['@nye'],
    'Citrus Wallet': ['@payu'],
    'EbixCash UPI': ['@ebixcash'],
    'Freecharge': ['@fcwallet'],
    'Airtel Payments Bank': ['@airtel'],
    'India Post Payments Bank': ['@ippb'],
    'FinoPay': ['@finobank'],
    'UltraCash': ['@ultracash'],
    'Jana Bank': ['@janabank'],
    'Samsung Pay': ['@pingpay'],
    'Zupee Ludo': ['@zupay'],
    # Bank UPI Handles
    'State Bank of India': ['@sbi'],
    'HDFC Bank': ['@hdfcbank'],
    'ICICI Bank': ['@icici'],
    'Axis Bank': ['@axisbank'],
    'Punjab National Bank': ['@pnb'],
    'Bank of Baroda': ['@barodampay', '@bob'],
    'Canara Bank': ['@cnrb'],
    'Union Bank of India': ['@unionbank', '@uboi'],
    'Indian Bank': ['@indianbank'],
    'IDFC FIRST Bank': ['@idfcbank'],
    'Federal Bank': ['@federal'],
    'IndusInd Bank': ['@indus'],
    'South Indian Bank': ['@sib'],
    'UCO Bank': ['@uco'],
    'Central Bank of India': ['@centralbank'],
    'Catholic Syrian Bank': ['@csbpay'],
    'DCB Bank': ['@dcb'],
    'Karnataka Bank': ['@kbl'],
    'Bank of Maharashtra': ['@mahb'],
    'HSBC Bank': ['@hsbc'],
    'Andhra Bank': ['@andb'],
    'Allahabad Bank': ['@allbank'],
    'Oriental Bank of Commerce': ['@obc'],
    'Vijaya Bank': ['@vijb'],
    'United Bank of India': ['@ubi']
}



async def fetch_digital_payment_data_async(session, api_url, headers, payload, mobile_number, upi_handle, platform):
    """Asynchronous function to fetch data for a single UPI handle"""
    try:
        async with session.post(api_url, headers=headers, json=payload) as response:
            response.raise_for_status()
            data = await response.json()

            if data['status'] == 1:
                return {
                    str(mobile_number) + upi_handle: {
                        'success': True,
                        'upi_handle': upi_handle,
                        'platform': platform,
                        'data': data
                    }
                }
            elif data['status'] == 403:
                raise Exception(data['message'])
                return
            return {}

            
    except aiohttp.ClientResponseError as e:
        return {
            str(mobile_number) + upi_handle: {
                'success': False,
                'upi_handle': upi_handle,
                'platform': platform,
                'error': f"API request failed: {str(e)}"
            }
        }
    except json.JSONDecodeError:
        raise Exception("Failed to parse API response")
        return {
            str(mobile_number) + upi_handle: {
                'success': False,
                'upi_handle': upi_handle,
                'platform': platform,
                'error': "Failed to parse API response"
            }
        }
    except Exception as e:
        raise Exception(str(e))
        return {
            str(mobile_number) + upi_handle: {
                'success': False,
                'upi_handle': upi_handle,
                'platform': platform,
                'error': f"Unexpected errorss: {str(e)}"
            }
        }

async def fetch_all_digital_payment_data_async(mobile_number, api_url, api_key):
    """Fetch all digital payment data asynchronously"""
    headers = {
        "authkey": api_key,
        "Content-Type": "application/json"
    }
    
    tasks = []
    async with aiohttp.ClientSession() as session:
        for platform, upi_handles_list in upi_handles.items():
            for upi_handle in upi_handles_list:
                payload = {
                    "digital_payment_id": str(mobile_number) + upi_handle,
                    "consent": "Y",
                    "consent_text": "We confirm obtaining valid customer consent to access/process their digital payment id data. Consent remains valid, informed, and unwithdrawn."
                }
                
                task = fetch_digital_payment_data_async(
                    session, api_url, headers, payload, mobile_number, upi_handle, platform
                )
                tasks.append(task)
        
        results = await asyncio.gather(*tasks)
        
        # Combine all results into a single dictionary
        combined_results = {}
        for result in results:
            combined_results.update(result)
        
        return combined_results

def fetch_digital_payment_analyser_data(mobile_number):
    """Fetch digital payment details for the mobile number"""
    api_url = os.getenv('DIGITAL_PAYMENT_ANALYSER_API_URL')
    api_key = os.getenv('DIGITAL_PAYMENT_ANALYSER_AUTH_KEY')
    
    # Run the async function using asyncio
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(fetch_all_digital_payment_data_async(mobile_number, api_url, api_key))
    loop.close()
    
    return result