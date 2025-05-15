from datetime import datetime

def transform_api_response(api_data, mobile_number):
    """
    Transform API response to match our expected format
    """
    # Ensure required fields exist
    if 'txn_id' not in api_data:
        api_data['txn_id'] = str(uuid.uuid4())
    
    if 'datetime' not in api_data:
        api_data['datetime'] = datetime.now().isoformat()
        
    if 'mobile_number' not in api_data:
        api_data['mobile_number'] = mobile_number
        
    return api_data

def prepare_client_response(api_data, mobile_number=None):
    """
    Prepare the response for the client
    """
    return {
        "mobileNumber": mobile_number or api_data.get('mobile_number'),
        "txnId": api_data.get('txn_id'),
        "apiCategory": api_data.get('api_category'),
        "apiName": api_data.get('api_name'),
        "billable": api_data.get('billable'),
        "message": api_data.get('message'),
        "status": api_data.get('status'),
        "datetime": api_data.get('datetime'),
        "result": api_data.get('result', {})
    }