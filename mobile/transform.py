import uuid
from datetime import datetime

def transform_api_response(api_data, mobile_number):
    """Transform API response to match our expected format"""
    if not isinstance(api_data, dict):
        raise ValueError("API data must be a dictionary")
        
    # Create a copy to avoid modifying the original data
    transformed_data = api_data.copy()
    
    # Ensure required fields exist
    if 'txn_id' not in transformed_data:
        transformed_data['txn_id'] = str(uuid.uuid4())
    
    if 'datetime' not in transformed_data:
        transformed_data['datetime'] = datetime.now().isoformat()
        
    if 'mobile_number' not in transformed_data:
        transformed_data['mobile_number'] = mobile_number

    # Ensure result field exists
    if 'result' not in transformed_data:
        transformed_data['result'] = {}
        
    return transformed_data

def prepare_client_response(api_data, mobile_number=None):
    """Prepare the response for the client"""
    if not isinstance(api_data, dict):
        raise ValueError("API data must be a dictionary")
        
    return {
        "mobileNumber": mobile_number or api_data.get('mobile_number'),
        "txnId": api_data.get('txn_id'),
        "apiCategory": api_data.get('api_category'),
        "apiName": api_data.get('api_name'),
        "billable": api_data.get('billable', False),
        "message": api_data.get('message', ''),
        "status": api_data.get('status'),
        "datetime": api_data.get('datetime'),
        "result": api_data.get('result', {})
    }