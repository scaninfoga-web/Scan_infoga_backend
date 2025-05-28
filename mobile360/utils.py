import requests
import os
import json
from datetime import datetime
from dotenv import load_dotenv
from .transform import transform_api_response, prepare_client_response

from .models import (
    EquifaxReport, BasicCreditInfo, InquiryPhone, InquiryRequestInfo, InquiryResponseHeader, ProductCode, PhoneType, IDDetail, Score, CreditReport, CIRReportData, Enquiry, EnquirySummary, IDAndContactInfo, AddressInfo,EmailAddressInfo, IdentityInfo, OtherId, PANId, PersonalInfo, PhoneInfo, OtherKeyInd, RecentActivities, RetailAccountDetail, RetailAccountsSummary, History48Month, ScoreDetail,ScoringElement,
)

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
        "mobile" : mobile_number,
        "name" : name,
        'docNumber': id_number,
        'docType': id_type,
        "consent": "Y",
        "consent_text":"We confirm obtaining valid customer consent to access/process their mobile and PAN/Aadhaar data. Consent remains valid, informed, and unwithdrawn."
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

def format_equifax_response(record):
    # Base response structure
    formatted_response = {
        "id_number": record.id_number,
        "id_type": record.id_type,
        "mobile": record.mobile,
        "txn_id": record.txn_id,
        "api_category": record.api_category,
        "api_name": record.api_name,
        "billable": record.billable,
        "message": record.message,
        "status": record.status,
        "datetime": record.datetime.isoformat(),
        "result": {}
    }
    
    # Add basic credit info
    if hasattr(record, 'basic_credit_info'):
        basic_info = record.basic_credit_info
        formatted_response["result"]["name"] = basic_info.name
        formatted_response["result"]["credit_score"] = basic_info.credit_score
        formatted_response["result"]["id_number"] = record.id_number
        formatted_response["result"]["id_type"] = record.id_type
        formatted_response["result"]["mobile"] = record.mobile
    
    # Add credit report info
    if hasattr(record, 'credit_report'):
        credit_report = {
            "InquiryResponseHeader": {},
            "InquiryRequestInfo": {},
            "Score": [],
            "CCRResponse": {
                "CIRReportDataLst": [],
                "Status": "1"
            }
        }
        
        # Add inquiry response header
        if hasattr(record, 'inquiry_response_header'):
            header = record.inquiry_response_header
            credit_report["InquiryResponseHeader"] = {
                "ClientID": header.client_id,
                "CustRefField": header.cust_ref_field,
                "ReportOrderNO": header.report_order_no,
                "SuccessCode": header.success_code,
                "Date": header.date.isoformat() if header.date else "",
                "Time": header.time,
                "ProductCode": [code.value for code in header.product_codes.all()]
            }
        
        # Add inquiry request info
        if hasattr(record, 'inquiry_request_info'):
            req_info = record.inquiry_request_info
            credit_report["InquiryRequestInfo"] = {
                "InquiryPurpose": req_info.inquiry_purpose,
                "TransactionAmount": req_info.transaction_amount,
                "FirstName": req_info.first_name,
                "InquiryPhones": [
                    {
                        "seq": phone.seq,
                        "PhoneType": [phone_type.value for phone_type in phone.phone_types.all()],
                        "Number": phone.number
                    } for phone in req_info.inquiry_phones.all()
                ],
                "IDDetails": [
                    {
                        "seq": id_detail.seq,
                        "IDType": id_detail.id_type,
                        "Source": id_detail.source
                    } for id_detail in req_info.id_details.all()
                ]
            }
        
        # Add scores
        credit_report["Score"] = [
            {
                "Type": score.type,
                "Version": score.version
            } for score in record.scores.all()
        ]
        
        # Add CIR Report Data
        cir_data_list = []
        for cir_data in record.credit_report.cir_report_data_list.all():
            cir_report_item = {
                "CIRReportData": {},
                "InquiryRequestInfo": {},
                "InquiryResponseHeader": {},
                "Score": []
            }
            
            # Add CIR Report Data detail
            cir_detail = {}
            
            # Add enquiry summary
            if hasattr(cir_data, 'enquiry_summary'):
                summary = cir_data.enquiry_summary
                cir_detail["EnquirySummary"] = {
                    "Past12Months": summary.past_12_months,
                    "Past24Months": summary.past_24_months,
                    "Past30Days": summary.past_30_days,
                    "Purpose": summary.purpose,
                    "Recent": summary.recent,
                    "Total": summary.total
                }
            
            # Add enquiries
            cir_detail["Enquiries"] = [
                {
                    "Amount": enquiry.amount,
                    "Date": enquiry.date.isoformat() if enquiry.date else "",
                    "Institution": enquiry.institution,
                    "RequestPurpose": enquiry.request_purpose,
                    "Time": enquiry.time,
                    "seq": enquiry.seq
                } for enquiry in cir_data.enquiries.all()
            ]
            
            # Add ID and Contact Info
            if hasattr(cir_data, 'id_and_contact_info'):
                id_contact = cir_data.id_and_contact_info
                id_contact_data = {
                    "AddressInfo": [
                        {
                            "Address": addr.address,
                            "Postal": addr.postal,
                            "ReportedDate": addr.reported_date.isoformat() if addr.reported_date else "",
                            "Seq": addr.seq,
                            "State": addr.state,
                            "Type": addr.type
                        } for addr in id_contact.address_info.all()
                    ],
                    "EmailAddressInfo": [
                        {
                            "EmailAddress": email.email_address,
                            "ReportedDate": email.reported_date.isoformat() if email.reported_date else "",
                            "seq": email.seq
                        } for email in id_contact.email_address_info.all()
                    ],
                    "PhoneInfo": [
                        {
                            "Number": phone.number,
                            "ReportedDate": phone.reported_date.isoformat() if phone.reported_date else "",
                            "seq": phone.seq,
                            "typeCode": phone.type_code
                        } for phone in id_contact.phone_info.all()
                    ]
                }
                
                # Add Identity Info
                if hasattr(id_contact, 'identity_info'):
                    identity = id_contact.identity_info
                    id_contact_data["IdentityInfo"] = {
                        "OtherId": [
                            {
                                "IdNumber": other.id_number,
                                "ReportedDate": other.reported_date.isoformat() if other.reported_date else "",
                                "seq": other.seq
                            } for other in identity.other_ids.all()
                        ],
                        "PANId": [
                            {
                                "IdNumber": pan.id_number,
                                "ReportedDate": pan.reported_date.isoformat() if pan.reported_date else "",
                                "seq": pan.seq
                            } for pan in identity.pan_ids.all()
                        ]
                    }
                
                # Add Personal Info
                if hasattr(id_contact, 'personal_info'):
                    person = id_contact.personal_info
                    id_contact_data["PersonalInfo"] = {
                        " AliasName": {},
                        "Age": {
                            "Age": person.age
                        },
                        "DateOfBirth": person.date_of_birth.isoformat() if person.date_of_birth else "",
                        "Gender": person.gender,
                        "Name": {
                            "FirstName": person.first_name,
                            "FullName": person.full_name,
                            "LastName": person.last_name,
                            "MiddleName": person.middle_name
                        },
                        "Occupation": person.occupation,
                        "PlaceOfBirthInfo": {},
                        "TotalIncome": person.total_income
                    }
                
                cir_detail["IDAndContactInfo"] = id_contact_data
            
            # Add Other Key Ind
            if hasattr(cir_data, 'other_key_ind'):
                key_ind = cir_data.other_key_ind
                cir_detail["OtherKeyInd"] = {
                    "AgeOfOldestTrade": key_ind.age_of_oldest_trade,
                    "AllLinesEVERWritten": key_ind.all_lines_ever_written,
                    "AllLinesEVERWrittenIn6Months": key_ind.all_lines_ever_written_in_6_months,
                    "AllLinesEVERWrittenIn9Months": key_ind.all_lines_ever_written_in_9_months,
                    "NumberOfOpenTrades": key_ind.number_of_open_trades
                }
            
            # Add Recent Activities
            if hasattr(cir_data, 'recent_activities'):
                activities = cir_data.recent_activities
                cir_detail["RecentActivities"] = {
                    "AccountsDeliquent": activities.accounts_deliquent,
                    "AccountsOpened": activities.accounts_opened,
                    "AccountsUpdated": activities.accounts_updated,
                    "TotalInquiries": activities.total_inquiries
                }
            
            # Add Retail Account Details
            if hasattr(cir_data, 'retail_account_details'):
                retail_accounts = []
                for account in cir_data.retail_account_details.all():
                    account_detail = {
                        "AccountNumber": account.account_number,
                        "AccountStatus": account.account_status,
                        "AccountType": account.account_type,
                        "Balance": account.balance,
                        "CreditLimit": account.credit_limit if account.credit_limit else "",
                        "DateOpened": account.date_opened.isoformat() if account.date_opened else "",
                        "DateReported": account.date_reported.isoformat() if account.date_reported else "",
                        "HighCredit": account.high_credit if account.high_credit else "",
                        "Institution": account.institution,
                        "LastPaymentDate": account.last_payment_date.isoformat() if account.last_payment_date else "",
                        "Open": account.open,
                        "OwnershipType": account.ownership_type,
                        "PastDueAmount": account.past_due_amount if account.past_due_amount else "",
                        "seq": account.seq,
                        "source": account.source
                    }
                    
                    # Add payment history
                    if hasattr(account, 'history_48_months'):
                        history = []
                        for month in account.history_48_months.all():
                            history.append({
                                "AssetClassificationStatus": month.asset_classification_status,
                                "PaymentStatus": month.payment_status,
                                "SuitFiledStatus": month.suit_filed_status,
                                "key": month.key
                            })
                        account_detail["History48Months"] = history
                    
                    retail_accounts.append(account_detail)
                
                cir_detail["RetailAccountDetails"] = retail_accounts
            
            # Add Retail Accounts Summary
            if hasattr(cir_data, 'retail_accounts_summary'):
                summary = cir_data.retail_accounts_summary
                cir_detail["RetailAccountsSummary"] = {
                    "AverageOpenBalance": summary.average_open_balance,
                    "MostSevereStatusWithIn24Months": summary.most_severe_status_within_24_months,
                    "NoOfAccounts": summary.no_of_accounts,
                    "NoOfActiveAccounts": summary.no_of_active_accounts,
                    "NoOfPastDueAccounts": summary.no_of_past_due_accounts,
                    "NoOfWriteOffs": summary.no_of_write_offs,
                    "NoOfZeroBalanceAccounts": summary.no_of_zero_balance_accounts,
                    "OldestAccount": summary.oldest_account,
                    "RecentAccount": summary.recent_account,
                    "SingleHighestBalance": summary.single_highest_balance,
                    "SingleHighestCredit": summary.single_highest_credit,
                    "SingleHighestSanctionAmount": summary.single_highest_sanction_amount,
                    "TotalBalanceAmount": summary.total_balance_amount,
                    "TotalCreditLimit": summary.total_credit_limit,
                    "TotalHighCredit": summary.total_high_credit,
                    "TotalMonthlyPaymentAmount": summary.total_monthly_payment_amount,
                    "TotalPastDue": summary.total_past_due,
                    "TotalSanctionAmount": summary.total_sanction_amount
                }
            
            # Add Score Details
            if hasattr(cir_data, 'score_details'):
                score_details = []
                for score in cir_data.score_details.all():
                    score_detail = {
                        "Name": score.name,
                        "Type": score.type,
                        "Value": score.value,
                        "Version": score.version
                    }
                    
                    # Add scoring elements
                    if hasattr(score, 'scoring_elements'):
                        elements = []
                        for element in score.scoring_elements.all():
                            elements.append({
                                "Description": element.description,
                                "code": element.code,
                                "seq": element.seq,
                                "type": element.type
                            })
                        score_detail["ScoringElements"] = elements
                    
                    score_details.append(score_detail)
                
                cir_detail["ScoreDetails"] = score_details
            
            # Assign the completed CIR detail to report item
            cir_report_item["CIRReportData"] = cir_detail
            
            # Add Inquiry Request Info for the CIR item
            if hasattr(cir_data, 'inquiry_request_info'):
                req = cir_data.inquiry_request_info
                cir_report_item["InquiryRequestInfo"] = {
                    "DOB": req.dob.isoformat() if hasattr(req, 'dob') and req.dob else "",
                    "FirstName": req.first_name,
                    "Gender": req.gender,
                    "InquiryPurpose": req.inquiry_purpose,
                    "TransactionAmount": req.transaction_amount
                }
                
                # Add ID Details
                if hasattr(req, 'id_details'):
                    cir_report_item["InquiryRequestInfo"]["IDDetails"] = [
                        {
                            "IDType": id_detail.id_type,
                            "IDValue": id_detail.id_value,
                            "seq": id_detail.seq
                        } for id_detail in req.id_details.all()
                    ]
                
                # Add Inquiry Addresses
                if hasattr(req, 'inquiry_addresses'):
                    cir_report_item["InquiryRequestInfo"]["InquiryAddresses"] = [
                        {
                            "AddressLine1": addr.address_line1,
                            "AddressType": [addr_type.value for addr_type in addr.address_types.all()],
                            "City": addr.city,
                            "Postal": addr.postal,
                            "State": addr.state,
                            "seq": addr.seq
                        } for addr in req.inquiry_addresses.all()
                    ]
                
                # Add Inquiry Phones
                if hasattr(req, 'inquiry_phones'):
                    cir_report_item["InquiryRequestInfo"]["InquiryPhones"] = [
                        {
                            "Number": phone.number,
                            "PhoneType": [phone_type.value for phone_type in phone.phone_types.all()],
                            "seq": phone.seq
                        } for phone in req.inquiry_phones.all()
                    ]
            
            # Add Inquiry Response Header for the CIR item
            if hasattr(cir_data, 'inquiry_response_header'):
                header = cir_data.inquiry_response_header
                cir_report_item["InquiryResponseHeader"] = {
                    "CustRefField": header.cust_ref_field,
                    "CustomerCode": header.customer_code,
                    "CustomerName": header.customer_name,
                    "Date": header.date.isoformat() if header.date else "",
                    "HitCode": header.hit_code,
                    "ProductCode": [code.value for code in header.product_codes.all()],
                    "ReportOrderNO": header.report_order_no,
                    "SuccessCode": header.success_code,
                    "Time": header.time
                }
            
            # Add Scores for the CIR item
            if hasattr(cir_data, 'scores'):
                cir_report_item["Score"] = [
                    {
                        "Type": score.type,
                        "Version": score.version
                    } for score in cir_data.scores.all()
                ]
            
            # Add completed CIR report item to the list
            cir_data_list.append(cir_report_item)
        
        # Add CIR report data list to CCR Response
        credit_report["CCRResponse"]["CIRReportDataLst"] = cir_data_list
        
        # Add complete credit report to result
        formatted_response["result"]["credit_report"] = credit_report
    
    return formatted_response

# Helper function to update an existing Equifax report record
def update_equifax_record(existing_record, data):
    try:
        # Extract main record fields
        result = data.get('result', {})
        
        # Update main record fields
        existing_record.txn_id = data.get('txn_id')
        existing_record.api_category = data.get('api_category')
        existing_record.api_name = data.get('api_name')
        existing_record.billable = data.get('billable')
        existing_record.message = data.get('message')
        existing_record.status = data.get('status')
        existing_record.mobile = result.get('mobile', existing_record.mobile)
        existing_record.save()
        
        # Update or create related basic credit info
        if hasattr(existing_record, 'basic_credit_info'):
            basic_info = existing_record.basic_credit_info
        else:
            basic_info = BasicCreditInfo(report=existing_record)
        
        basic_info.name = result.get('name', '')
        basic_info.credit_score = result.get('credit_score', '')
        basic_info.save()
        
        # Update credit report and related models
        credit_report_data = result.get('credit_report', {})
        
        if credit_report_data and hasattr(existing_record, 'credit_report'):
            update_credit_report(existing_record.credit_report, credit_report_data)
        elif credit_report_data:
            create_credit_report(existing_record, credit_report_data)
        
        return True
    except Exception as e:
        # Log the error
        print(f"Error updating Equifax record: {str(e)}")
        raise

def create_equifax_record(data):
    try:
        # Extract main record fields
        result = data.get('result', {})
        
        # Create main record
        new_record = EquifaxReport(
            id_number=result.get('id_number'),
            id_type=result.get('id_type'),
            mobile=result.get('mobile', ''),
            txn_id=data.get('txn_id'),
            api_category=data.get('api_category'),
            api_name=data.get('api_name'),
            billable=data.get('billable'),
            message=data.get('message'),
            status=data.get('status'),
            datetime=datetime.fromisoformat(data.get('datetime')) if isinstance(data.get('datetime'), str) else data.get('datetime')
        )
        new_record.save()
        
        # Create basic credit info
        BasicCreditInfo.objects.create(
            report=new_record,  # Changed from equifax_report to report
            name=result.get('name', ''),
            credit_score=result.get('credit_score', '')
        )
        
        # Create credit report and related models
        credit_report_data = result.get('credit_report', {})
        
        if credit_report_data:
            create_credit_report(new_record, credit_report_data)
        
        return new_record
    except Exception as e:
        # Log the error
        print(f"Error creating Equifax record: {str(e)}")
        raise

# Helper function to create credit report and related models
def create_credit_report(equifax_record, credit_report_data):
    # Create main credit report
    credit_report = CreditReport.objects.create(report=equifax_record)
    
    # Create inquiry response header
    header_data = credit_report_data.get('InquiryResponseHeader', {})
    if header_data:
        header = InquiryResponseHeader.objects.create(
            report=equifax_record,  # Changed from credit_report to equifax_record
            client_id=header_data.get('ClientID', ''),
            cust_ref_field=header_data.get('CustRefField', ''),
            report_order_no=header_data.get('ReportOrderNO', ''),
            success_code=header_data.get('SuccessCode', ''),
            date=datetime.fromisoformat(header_data.get('Date')) if header_data.get('Date') else None,
            time=header_data.get('Time', '')
        )
        
        # Create product codes
        for code_value in header_data.get('ProductCode', []):
            ProductCode.objects.create(
                response_header=header,
                value=code_value
            )
    
    # Create inquiry request info
    req_data = credit_report_data.get('InquiryRequestInfo', {})
    if req_data:
        req_info = InquiryRequestInfo.objects.create(
            report=credit_report,
            inquiry_purpose=req_data.get('InquiryPurpose', ''),
            transaction_amount=req_data.get('TransactionAmount', ''),
            first_name=req_data.get('FirstName', '')
        )
        
        # Create inquiry phones
        for phone_data in req_data.get('InquiryPhones', []):
            phone = InquiryPhone.objects.create(
                request_info=req_info,
                seq=phone_data.get('seq', ''),
                number=phone_data.get('Number', '')
            )
            
            # Create phone types
            for type_value in phone_data.get('PhoneType', []):
                PhoneType.objects.create(
                    inquiry_phone=phone,
                    value=type_value
                )
        
        # Create ID details
        for id_data in req_data.get('IDDetails', []):
            IDDetail.objects.create(
                request_info=req_info,
                seq=id_data.get('seq', ''),
                id_type=id_data.get('IDType', ''),
                source=id_data.get('Source', '')
            )
    
    # Create scores
    for score_data in credit_report_data.get('Score', []):
        Score.objects.create(
            report=credit_report,
            type=score_data.get('Type', ''),
            version=score_data.get('Version', '')
        )
    
    # Create CIR report data
    for cir_data in credit_report_data.get('CCRResponse', {}).get('CIRReportDataLst', []):
        create_cir_report_data(credit_report, cir_data)
    
    return credit_report

# Helper function to create CIR report data and related models
def create_cir_report_data(credit_report, cir_data):
    # Create main CIR report data
    cir_record = CIRReportData.objects.create(credit_report=credit_report)
    
    cir_report_data = cir_data.get('CIRReportData', {})
    
    # Create enquiry summary
    if 'EnquirySummary' in cir_report_data:
        summary_data = cir_report_data.get('EnquirySummary', {})
        EnquirySummary.objects.create(
            cir_report_data=cir_record,
            past_12_months=summary_data.get('Past12Months', ''),
            past_24_months=summary_data.get('Past24Months', ''),
            past_30_days=summary_data.get('Past30Days', ''),
            purpose=summary_data.get('Purpose', ''),
            recent=summary_data.get('Recent', ''),
            total=summary_data.get('Total', '')
        )
    
    # Create enquiries
    for enquiry_data in cir_report_data.get('Enquiries', []):
        Enquiry.objects.create(
            cir_report_data=cir_record,
            amount=enquiry_data.get('Amount', ''),
            date=datetime.fromisoformat(enquiry_data.get('Date')) if enquiry_data.get('Date') else None,
            institution=enquiry_data.get('Institution', ''),
            request_purpose=enquiry_data.get('RequestPurpose', ''),
            time=enquiry_data.get('Time', ''),
            seq=enquiry_data.get('seq', '')
        )
    
    # Create ID and contact info
    if 'IDAndContactInfo' in cir_report_data:
        id_contact_data = cir_report_data.get('IDAndContactInfo', {})
        id_contact = IDAndContactInfo.objects.create(cir_report_data=cir_record)
        
        # Create address info
        for addr_data in id_contact_data.get('AddressInfo', []):
            AddressInfo.objects.create(
                id_and_contact_info=id_contact,
                address=addr_data.get('Address', ''),
                postal=addr_data.get('Postal', ''),
                reported_date=datetime.fromisoformat(addr_data.get('ReportedDate')) if addr_data.get('ReportedDate') else None,
                seq=addr_data.get('Seq', ''),
                state=addr_data.get('State', ''),
                type=addr_data.get('Type', '')
            )
        
        # Create email address info
        for email_data in id_contact_data.get('EmailAddressInfo', []):
            EmailAddressInfo.objects.create(
                id_and_contact_info=id_contact,
                email_address=email_data.get('EmailAddress', ''),
                reported_date=datetime.fromisoformat(email_data.get('ReportedDate')) if email_data.get('ReportedDate') else None,
                seq=email_data.get('seq', '')
            )
        
        # Create phone info
        for phone_data in id_contact_data.get('PhoneInfo', []):
            PhoneInfo.objects.create(
                id_and_contact_info=id_contact,
                number=phone_data.get('Number', ''),
                reported_date=datetime.fromisoformat(phone_data.get('ReportedDate')) if phone_data.get('ReportedDate') else None,
                seq=phone_data.get('seq', ''),
                type_code=phone_data.get('typeCode', '')
            )
        
        # Create identity info
        if 'IdentityInfo' in id_contact_data:
            identity_data = id_contact_data.get('IdentityInfo', {})
            identity = IdentityInfo.objects.create(id_and_contact_info=id_contact)
            
            # Create PAN IDs
            for pan_data in identity_data.get('PANId', []):
                PANId.objects.create(
                    identity_info=identity,
                    id_number=pan_data.get('IdNumber', ''),
                    reported_date=datetime.fromisoformat(pan_data.get('ReportedDate')) if pan_data.get('ReportedDate') else None,
                    seq=pan_data.get('seq', '')
                )
            
            # Create Other IDs
            for other_data in identity_data.get('OtherId', []):
                OtherId.objects.create(
                    identity_info=identity,
                    id_number=other_data.get('IdNumber', ''),
                    reported_date=datetime.fromisoformat(other_data.get('ReportedDate')) if other_data.get('ReportedDate') else None,
                    seq=other_data.get('seq', '')
                )
        
        # Create personal info
        if 'PersonalInfo' in id_contact_data:
            person_data = id_contact_data.get('PersonalInfo', {})
            PersonalInfo.objects.create(
                id_and_contact_info=id_contact,
                age=person_data.get('Age', {}).get('Age', ''),
                date_of_birth=datetime.fromisoformat(person_data.get('DateOfBirth')) if person_data.get('DateOfBirth') else None,
                gender=person_data.get('Gender', ''),
                first_name=person_data.get('Name', {}).get('FirstName', ''),
                full_name=person_data.get('Name', {}).get('FullName', ''),
                last_name=person_data.get('Name', {}).get('LastName', ''),
                middle_name=person_data.get('Name', {}).get('MiddleName', ''),
                occupation=person_data.get('Occupation', ''),
                total_income=person_data.get('TotalIncome', '')
            )
    
    # Create OtherKeyInd
    if 'OtherKeyInd' in cir_report_data:
        key_ind_data = cir_report_data.get('OtherKeyInd', {})
        OtherKeyInd.objects.create(
            cir_report_data=cir_record,
            age_of_oldest_trade=key_ind_data.get('AgeOfOldestTrade', ''),
            all_lines_ever_written=key_ind_data.get('AllLinesEVERWritten', ''),
            all_lines_ever_written_in_6_months=key_ind_data.get('AllLinesEVERWrittenIn6Months', ''),
            all_lines_ever_written_in_9_months=key_ind_data.get('AllLinesEVERWrittenIn9Months', ''),
            number_of_open_trades=key_ind_data.get('NumberOfOpenTrades', '')
        )
    
    # Create RecentActivities
    if 'RecentActivities' in cir_report_data:
        activities_data = cir_report_data.get('RecentActivities', {})
        RecentActivities.objects.create(
            cir_report_data=cir_record,
            accounts_deliquent=activities_data.get('AccountsDeliquent', ''),
            accounts_opened=activities_data.get('AccountsOpened', ''),
            accounts_updated=activities_data.get('AccountsUpdated', ''),
            total_inquiries=activities_data.get('TotalInquiries', '')
        )
    
    # Create RetailAccountsSummary
    if 'RetailAccountsSummary' in cir_report_data:
        summary_data = cir_report_data.get('RetailAccountsSummary', {})
        RetailAccountsSummary.objects.create(
            cir_report_data=cir_record,
            average_open_balance=summary_data.get('AverageOpenBalance', ''),
            most_severe_status_within_24_months=summary_data.get('MostSevereStatusWithIn24Months', ''),
            no_of_accounts=summary_data.get('NoOfAccounts', ''),
            no_of_active_accounts=summary_data.get('NoOfActiveAccounts', ''),
            no_of_past_due_accounts=summary_data.get('NoOfPastDueAccounts', ''),
            no_of_write_offs=summary_data.get('NoOfWriteOffs', ''),
            no_of_zero_balance_accounts=summary_data.get('NoOfZeroBalanceAccounts', ''),
            oldest_account=summary_data.get('OldestAccount', ''),
            recent_account=summary_data.get('RecentAccount', ''),
            single_highest_balance=summary_data.get('SingleHighestBalance', ''),
            single_highest_credit=summary_data.get('SingleHighestCredit', ''),
            single_highest_sanction_amount=summary_data.get('SingleHighestSanctionAmount', ''),
            total_balance_amount=summary_data.get('TotalBalanceAmount', ''),
            total_credit_limit=summary_data.get('TotalCreditLimit', ''),
            total_high_credit=summary_data.get('TotalHighCredit', ''),
            total_monthly_payment_amount=summary_data.get('TotalMonthlyPaymentAmount', ''),
            total_past_due=summary_data.get('TotalPastDue', ''),
            total_sanction_amount=summary_data.get('TotalSanctionAmount', '')
        )
    
    # Create RetailAccountDetails
    for account_data in cir_report_data.get('RetailAccountDetails', []):
        account = RetailAccountDetail.objects.create(
            cir_report_data=cir_record,
            account_number=account_data.get('AccountNumber', ''),
            account_status=account_data.get('AccountStatus', ''),
            account_type=account_data.get('AccountType', ''),
            balance=account_data.get('Balance', ''),
            credit_limit=account_data.get('CreditLimit', ''),
            date_opened=datetime.fromisoformat(account_data.get('DateOpened')) if account_data.get('DateOpened') else None,
            date_reported=datetime.fromisoformat(account_data.get('DateReported')) if account_data.get('DateReported') else None,
            high_credit=account_data.get('HighCredit', ''),
            institution=account_data.get('Institution', ''),
            last_payment_date=datetime.fromisoformat(account_data.get('LastPaymentDate')) if account_data.get('LastPaymentDate') else None,
            open=account_data.get('Open', ''),
            ownership_type=account_data.get('OwnershipType', ''),
            past_due_amount=account_data.get('PastDueAmount', ''),
            seq=account_data.get('seq', ''),
            source=account_data.get('source', '')
        )
        
        # Create History48Months
        for month_data in account_data.get('History48Months', []):
            History48Month.objects.create(
                retail_account=account,
                asset_classification_status=month_data.get('AssetClassificationStatus', ''),
                payment_status=month_data.get('PaymentStatus', ''),
                suit_filed_status=month_data.get('SuitFiledStatus', ''),
                key=month_data.get('key', '')
            )
    
    # Create ScoreDetails
    for score_data in cir_report_data.get('ScoreDetails', []):
        score_detail = ScoreDetail.objects.create(
            cir_report_data=cir_record,
            name=score_data.get('Name', ''),
            type=score_data.get('Type', ''),
            value=score_data.get('Value', ''),
            version=score_data.get('Version', '')
        )
        
        # Create ScoringElements
        for element_data in score_data.get('ScoringElements', []):
            ScoringElement.objects.create(
                score_detail=score_detail,
                description=element_data.get('Description', ''),
                code=element_data.get('code', ''),
                seq=element_data.get('seq', ''),
                type=element_data.get('type', '')
            )
    
    # Create Inquiry Request Info for the CIR item
    if 'InquiryRequestInfo' in cir_data:
        req_data = cir_data.get('InquiryRequestInfo', {})
        req = CIRInquiryRequestInfo.objects.create(
            cir_report_data=cir_record,
            dob=datetime.fromisoformat(req_data.get('DOB')) if req_data.get('DOB') else None,
            first_name=req_data.get('FirstName', ''),
            gender=req_data.get('Gender', ''),
            inquiry_purpose=req_data.get('InquiryPurpose', ''),
            transaction_amount=req_data.get('TransactionAmount', '')
        )
        
        # Create ID Details
        for id_data in req_data.get('IDDetails', []):
            CIRIDDetail.objects.create(
                inquiry_request=req,
                id_type=id_data.get('IDType', ''),
                id_value=id_data.get('IDValue', ''),
                seq=id_data.get('seq', '')
            )
        
        # Create Inquiry Addresses
        for addr_data in req_data.get('InquiryAddresses', []):
            address = CIRInquiryAddress.objects.create(
                inquiry_request=req,
                address_line1=addr_data.get('AddressLine1', ''),
                city=addr_data.get('City', ''),
                postal=addr_data.get('Postal', ''),
                state=addr_data.get('State', ''),
                seq=addr_data.get('seq', '')
            )
            
            # Create address types
            for type_value in addr_data.get('AddressType', []):
                CIRAddressType.objects.create(
                    address=address,
                    value=type_value
                )
        
        # Create Inquiry Phones
        for phone_data in req_data.get('InquiryPhones', []):
            phone = CIRInquiryPhone.objects.create(
                inquiry_request=req,
                number=phone_data.get('Number', ''),
                seq=phone_data.get('seq', '')
            )
            
            # Create phone types
            for type_value in phone_data.get('PhoneType', []):
                CIRPhoneType.objects.create(
                    phone=phone,
                    value=type_value
                )
    
    # Create Inquiry Response Header for the CIR item
    if 'InquiryResponseHeader' in cir_data:
        header_data = cir_data.get('InquiryResponseHeader', {})
        header = CIRInquiryResponseHeader.objects.create(
            cir_report_data=cir_record,
            cust_ref_field=header_data.get('CustRefField', ''),
            customer_code=header_data.get('CustomerCode', ''),
            customer_name=header_data.get('CustomerName', ''),
            date=datetime.fromisoformat(header_data.get('Date')) if header_data.get('Date') else None,
            hit_code=header_data.get('HitCode', ''),
            report_order_no=header_data.get('ReportOrderNO', ''),
            success_code=header_data.get('SuccessCode', ''),
            time=header_data.get('Time', '')
        )
        
        # Create product codes
        for code_value in header_data.get('ProductCode', []):
            CIRProductCode.objects.create(
                header=header,
                value=code_value
            )
    
    # Create Scores for the CIR item
    for score_data in cir_data.get('Score', []):
        CIRScore.objects.create(
            cir_report_data=cir_record,
            type=score_data.get('Type', ''),
            version=score_data.get('Version', '')
        )
    
    return cir_record

# Helper function to update an existing credit report
def update_credit_report(credit_report, credit_report_data):
    # Update inquiry response header
    header_data = credit_report_data.get('InquiryResponseHeader', {})
    if header_data:
        if hasattr(credit_report, 'inquiry_response_header'):
            header = credit_report.inquiry_response_header
            header.client_id = header_data.get('ClientID', header.client_id)
            header.cust_ref_field = header_data.get('CustRefField', header.cust_ref_field)
            header.report_order_no = header_data.get('ReportOrderNO', header.report_order_no)
            header.success_code = header_data.get('SuccessCode', header.success_code)
            header.date = datetime.fromisoformat(header_data.get('Date')) if header_data.get('Date') else header.date
            header.time = header_data.get('Time', header.time)
            header.save()
            
            # Update product codes
            header.product_codes.all().delete()
            for code_value in header_data.get('ProductCode', []):
                ProductCode.objects.create(
                    header=header,
                    value=code_value
                )
        else:
            # Create new header if it doesn't exist
            header = InquiryResponseHeader.objects.create(
                report=credit_report.report,  # Changed from credit_report to credit_report.report to get the EquifaxReport instance
                client_id=header_data.get('ClientID', ''),
                cust_ref_field=header_data.get('CustRefField', ''),
                report_order_no=header_data.get('ReportOrderNO', ''),
                success_code=header_data.get('SuccessCode', ''),
                date=datetime.fromisoformat(header_data.get('Date')) if header_data.get('Date') else None,
                time=header_data.get('Time', '')
            )
            
            # Create product codes
            for code_value in header_data.get('ProductCode', []):
                ProductCode.objects.create(
                    response_header=header,
                    value=code_value
                )
    
    # Update inquiry request info
    req_data = credit_report_data.get('InquiryRequestInfo', {})
    if req_data:
        if hasattr(credit_report, 'inquiry_request_info'):
            req_info = credit_report.inquiry_request_info
            req_info.inquiry_purpose = req_data.get('InquiryPurpose', req_info.inquiry_purpose)
            req_info.transaction_amount = req_data.get('TransactionAmount', req_info.transaction_amount)
            req_info.first_name = req_data.get('FirstName', req_info.first_name)
            req_info.save()
            
            # Update inquiry phones
            req_info.inquiry_phones.all().delete()
            for phone_data in req_data.get('InquiryPhones', []):
                phone = InquiryPhone.objects.create(
                    request_info=req_info,
                    seq=phone_data.get('seq', ''),
                    number=phone_data.get('Number', '')
                )
                
                # Create phone types
                for type_value in phone_data.get('PhoneType', []):
                    PhoneType.objects.create(
                        inquiry_phone=phone,
                        value=type_value
                    )
            
            # Update ID details
            req_info.id_details.all().delete()
            for id_data in req_data.get('IDDetails', []):
                IDDetail.objects.create(
                    request_info=req_info,
                    seq=id_data.get('seq', ''),
                    id_type=id_data.get('IDType', ''),
                    source=id_data.get('Source', '')
                )
        else:
            # Create new request info if it doesn't exist
            req_info = InquiryRequestInfo.objects.create(
                report=credit_report,
                inquiry_purpose=req_data.get('InquiryPurpose', ''),
                transaction_amount=req_data.get('TransactionAmount', ''),
                first_name=req_data.get('FirstName', '')
            )
            
            # Create inquiry phones
            for phone_data in req_data.get('InquiryPhones', []):
                phone = InquiryPhone.objects.create(
                    request_info=req_info,
                    seq=phone_data.get('seq', ''),
                    number=phone_data.get('Number', '')
                )
                
                # Create phone types
                for type_value in phone_data.get('PhoneType', []):
                    PhoneType.objects.create(
                        inquiry_phone=phone,
                        value=type_value
                    )
            
            # Create ID details
            for id_data in req_data.get('IDDetails', []):
                IDDetail.objects.create(
                    request_info=req_info,
                    seq=id_data.get('seq', ''),
                    id_type=id_data.get('IDType', ''),
                    source=id_data.get('Source', '')
                )
    
    # Update scores
    credit_report.scores.all().delete()
    for score_data in credit_report_data.get('Score', []):
        Score.objects.create(
            report=credit_report,
            type=score_data.get('Type', ''),
            version=score_data.get('Version', '')
        )
    
    # Update CIR report data
    # First, delete all existing CIR reports
    credit_report.cir_report_data_list.all().delete()
    
    # Create new CIR reports
    for cir_data in credit_report_data.get('CCRResponse', {}).get('CIRReportDataLst', []):
        create_cir_report_data(credit_report, cir_data)
    
    return credit_report


