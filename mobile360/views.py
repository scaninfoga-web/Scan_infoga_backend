from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from core.utils import create_response
import uuid
from django.utils import timezone
from django.db import transaction

from .models import (
    Mobile360, DigitalPaymentInfo, LPGInfo, TelcoInfo,
    MobileAgeInfo, WhatsappInfo, RevokeInfo, KeyHighlights,
    UanHistoryLatestV2,UanEmploymentHistory, GstVerification, EsicDtls, GstTurnover,
    UdyamDetails, UdyamAddress, UdyamEnterpriseType, UdyamNICCode, UdyamPlantDetail,
    MobileToAccountDetails, AccountDetails, VpaDetails
)
from .utils import (
    fetch_mobile360_data, fetch_uan_employment_data, fetch_uan_history_data, fetch_esic_data, fetch_gst_data, fetch_gst_turnover_data, fetch_udyam_data, fetch_mobile_to_account_data
)

@api_view(['POST'])
def mobile_360_search(request):
    try:
        mobile_number = request.data.get('mobileNumber')
        realtime_data = request.data.get('realtimeData', False)

        if not mobile_number:
            return Response({
                'status': False,
                'message': 'Mobile number is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Check if data exists in database
        existing_data = None
        existing_mobile_360 = None
        
        try:
            existing_mobile_360 = Mobile360.objects.get(mobile_number=mobile_number)
            
            # If not requesting realtime data, return existing data
            if not realtime_data:
                # Construct response from database
                existing_data = {
                    "mobileNumber": mobile_number,
                    "txnId": str(existing_mobile_360.txn_id),
                    "apiCategory": existing_mobile_360.api_category,
                    "apiName": existing_mobile_360.api_name,
                    "billable": existing_mobile_360.billable,
                    "message": existing_mobile_360.message,
                    "status": existing_mobile_360.status,
                    "datetime": existing_mobile_360.datetime.isoformat(),
                    "result": {
                        "digital_payment_id_info": {
                            "code": existing_mobile_360.digital_payment_info.code if hasattr(existing_mobile_360, 'digital_payment_info') else "NRF",
                            "data": {
                                "name": existing_mobile_360.digital_payment_info.name,
                                "bank": existing_mobile_360.digital_payment_info.bank,
                                "branch": existing_mobile_360.digital_payment_info.branch,
                                "center": existing_mobile_360.digital_payment_info.center,
                                "district": existing_mobile_360.digital_payment_info.district,
                                "state": existing_mobile_360.digital_payment_info.state,
                                "address": existing_mobile_360.digital_payment_info.address,
                                "contact": existing_mobile_360.digital_payment_info.contact,
                                "city": existing_mobile_360.digital_payment_info.city
                            } if hasattr(existing_mobile_360, 'digital_payment_info') else {}
                        },
                        "lpg_info": {
                            "code": "SUC" if existing_mobile_360.lpg_info.exists() else "NRF",
                            "data": [{
                                "gas_provider": lpg.gas_provider,
                                "name": lpg.name,
                                "consumer_details": {
                                    "consumer_mobile": lpg.consumer_mobile,
                                    "consumer_id": lpg.consumer_id,
                                    "consumer_status": lpg.consumer_status,
                                    "consumer_type": lpg.consumer_type
                                },
                                "address": lpg.address,
                                "distributor_details": {
                                    "distributor_code": lpg.distributor_code,
                                    "distributor_name": lpg.distributor_name,
                                    "distributor_contact": lpg.distributor_contact,
                                    "distributor_address": lpg.distributor_address
                                }
                            } for lpg in existing_mobile_360.lpg_info.all()]
                        },
                        "telco_info": {
                            "code": existing_mobile_360.telco_info.code if hasattr(existing_mobile_360, 'telco_info') else "NRF",
                            "data": {
                                "is_valid": existing_mobile_360.telco_info.is_valid,
                                "subscriber_status": existing_mobile_360.telco_info.subscriber_status,
                                "connection_type": existing_mobile_360.telco_info.connection_type,
                                "msisdn": {
                                    "msisdn": existing_mobile_360.telco_info.msisdn,
                                    "msisdn_country_code": existing_mobile_360.telco_info.msisdn_country_code
                                },
                                "current_service_provider": {
                                    "network_name": existing_mobile_360.telco_info.network_name,
                                    "network_region": existing_mobile_360.telco_info.network_region
                                },
                                "is_roaming": existing_mobile_360.telco_info.is_roaming
                            } if hasattr(existing_mobile_360, 'telco_info') else {}
                        },
                        "mobile_age_info": {
                            "code": existing_mobile_360.mobile_age_info.code if hasattr(existing_mobile_360, 'mobile_age_info') else "NRF",
                            "data": {
                                "is_ported": existing_mobile_360.mobile_age_info.is_ported,
                                "mobile_age": existing_mobile_360.mobile_age_info.mobile_age,
                                "number_active": existing_mobile_360.mobile_age_info.number_active,
                                "number_valid": existing_mobile_360.mobile_age_info.number_valid,
                                "ported_region": existing_mobile_360.mobile_age_info.ported_region,
                                "ported_telecom": existing_mobile_360.mobile_age_info.ported_telecom,
                                "region": existing_mobile_360.mobile_age_info.region,
                                "roaming": existing_mobile_360.mobile_age_info.roaming,
                                "telecom": existing_mobile_360.mobile_age_info.telecom
                            } if hasattr(existing_mobile_360, 'mobile_age_info') else {}
                        },
                        "whatsapp_info": {
                            "code": existing_mobile_360.whatsapp_info.code if hasattr(existing_mobile_360, 'whatsapp_info') else "NRF",
                            "data": {
                                "status": existing_mobile_360.whatsapp_info.status,
                                "is_business": existing_mobile_360.whatsapp_info.is_business
                            } if hasattr(existing_mobile_360, 'whatsapp_info') else {}
                        },
                        "revoke_info": {
                            "code": existing_mobile_360.revoke_info.code if hasattr(existing_mobile_360, 'revoke_info') else "NRF",
                            "data": {
                                "revoke_date": existing_mobile_360.revoke_info.revoke_date,
                                "revoke_status": existing_mobile_360.revoke_info.revoke_status
                            } if hasattr(existing_mobile_360, 'revoke_info') else {}
                        },
                        "key_highlights": {
                            "digital_payment_id_name": existing_mobile_360.key_highlights.digital_payment_id_name if hasattr(existing_mobile_360, 'key_highlights') else "",
                            "gas_connection_found": existing_mobile_360.key_highlights.gas_connection_found if hasattr(existing_mobile_360, 'key_highlights') else "",
                            "connection_type": existing_mobile_360.key_highlights.connection_type if hasattr(existing_mobile_360, 'key_highlights') else "",
                            "whatsapp_business_account_status": existing_mobile_360.key_highlights.whatsapp_business_account_status if hasattr(existing_mobile_360, 'key_highlights') else "",
                            "age_of_mobile": existing_mobile_360.key_highlights.age_of_mobile if hasattr(existing_mobile_360, 'key_highlights') else "",
                            "active_status": existing_mobile_360.key_highlights.active_status if hasattr(existing_mobile_360, 'key_highlights') else "",
                            "revoke_date": existing_mobile_360.key_highlights.revoke_date if hasattr(existing_mobile_360, 'key_highlights') else ""
                        }
                    }
                }
                
                return Response(
                    create_response(
                        status=True,
                        message='Data retrieved from database',
                        data=existing_data
                    ), 
                    status=status.HTTP_200_OK
                )
        except Mobile360.DoesNotExist:
            existing_mobile_360 = None

        # Call external API if no existing data or realtime_data is True
        api_response = fetch_mobile360_data(mobile_number)
        
        # Return early if the API call was unsuccessful
        if not api_response['success']:
            return Response(
                create_response(
                    status=False,
                    message=api_response['error'],
                    data=None
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Get the API response data
        api_data = api_response['data']
        
        # Additional check to ensure the status is 1 (success)
        if api_data['status'] != 1:
            return Response(
                create_response(
                    status=False,
                    message=f"API returned non-success status: {api_data['status']} - {api_data['message']}",
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Transaction handling for database operations
        with transaction.atomic():
            # If record exists, update it instead of creating a new one
            if existing_mobile_360:
                # Update the main Mobile360 record
                existing_mobile_360.txn_id = api_data.get('txnId')
                existing_mobile_360.api_category = api_data.get('apiCategory', '')
                existing_mobile_360.api_name = api_data.get('apiName', '')
                existing_mobile_360.billable = api_data.get('billable', False)
                existing_mobile_360.message = api_data.get('message', '')
                existing_mobile_360.status = api_data.get('status', 0)
                existing_mobile_360.datetime = datetime.fromisoformat(api_data.get('datetime')) if isinstance(api_data.get('datetime'), str) else api_data.get('datetime', datetime.now())
                existing_mobile_360.save()
                
                mobile_360 = existing_mobile_360
                
                # Delete existing related records to avoid duplicates
                if hasattr(mobile_360, 'digital_payment_info'):
                    mobile_360.digital_payment_info.delete()
                
                mobile_360.lpg_info.all().delete()
                
                if hasattr(mobile_360, 'telco_info'):
                    mobile_360.telco_info.delete()
                
                if hasattr(mobile_360, 'mobile_age_info'):
                    mobile_360.mobile_age_info.delete()
                
                if hasattr(mobile_360, 'whatsapp_info'):
                    mobile_360.whatsapp_info.delete()
                
                if hasattr(mobile_360, 'revoke_info'):
                    mobile_360.revoke_info.delete()
                
                if hasattr(mobile_360, 'key_highlights'):
                    mobile_360.key_highlights.delete()
            else:
                # Create new Mobile360 record if it doesn't exist
                mobile_360 = Mobile360.objects.create(
                    mobile_number=mobile_number,
                    txn_id=api_data.get('txnId'),
                    api_category=api_data.get('apiCategory', ''),
                    api_name=api_data.get('apiName', ''),
                    billable=api_data.get('billable', False),
                    message=api_data.get('message', ''),
                    status=api_data.get('status', 0),
                    datetime=datetime.fromisoformat(api_data.get('datetime')) if isinstance(api_data.get('datetime'), str) else api_data.get('datetime', datetime.now())
                )

            # Save Digital Payment Info if available with SUC code
            if api_data.get('result', {}).get('digital_payment_id_info', {}).get('code') == 'SUC':
                payment_data = api_data['result']['digital_payment_id_info'].get('data', {})
                DigitalPaymentInfo.objects.create(
                    mobile_response=mobile_360,
                    code=api_data['result']['digital_payment_id_info'].get('code', 'NRF'),
                    name=payment_data.get('name', ''),
                    bank=payment_data.get('bank', ''),
                    branch=payment_data.get('branch', ''),
                    center=payment_data.get('center', ''),
                    district=payment_data.get('district', ''),
                    state=payment_data.get('state', ''),
                    address=payment_data.get('address', ''),
                    contact=payment_data.get('contact', ''),
                    city=payment_data.get('city', '')
                )

            # Save LPG Info if available with SUC code
            if api_data.get('result', {}).get('lpg_info', {}).get('code') == 'SUC':
                lpg_list = api_data['result']['lpg_info'].get('data', [])
                for lpg_data in lpg_list:
                    consumer_details = lpg_data.get('consumer_details', {})
                    distributor_details = lpg_data.get('distributor_details', {})
                    
                    LPGInfo.objects.create(
                        mobile_response=mobile_360,
                        code=api_data['result']['lpg_info'].get('code', 'NRF'),
                        gas_provider=lpg_data.get('gas_provider', ''),
                        name=lpg_data.get('name', ''),
                        consumer_mobile=consumer_details.get('consumer_mobile', ''),
                        consumer_id=consumer_details.get('consumer_id', ''),
                        consumer_status=consumer_details.get('consumer_status', ''),
                        consumer_type=consumer_details.get('consumer_type', ''),
                        address=lpg_data.get('address', ''),
                        distributor_code=distributor_details.get('distributor_code', ''),
                        distributor_name=distributor_details.get('distributor_name', ''),
                        distributor_contact=distributor_details.get('distributor_contact', ''),
                        distributor_address=distributor_details.get('distributor_address', '')
                    )

            # Save Telco Info if available with SUC code
            if api_data.get('result', {}).get('telco_info', {}).get('code') == 'SUC':
                telco_data = api_data['result']['telco_info'].get('data', {})
                msisdn_data = telco_data.get('msisdn', {})
                service_provider = telco_data.get('current_service_provider', {})
                
                TelcoInfo.objects.create(
                    mobile_response=mobile_360,
                    code=api_data['result']['telco_info'].get('code', 'NRF'),
                    is_valid=telco_data.get('is_valid', False),
                    subscriber_status=telco_data.get('subscriber_status', ''),
                    connection_type=telco_data.get('connection_type', ''),
                    msisdn=msisdn_data.get('msisdn', ''),
                    msisdn_country_code=msisdn_data.get('msisdn_country_code', ''),
                    network_name=service_provider.get('network_name', ''),
                    network_region=service_provider.get('network_region', ''),
                    is_roaming=telco_data.get('is_roaming', False)
                )

            # Save Mobile Age Info if available with SUC code
            if api_data.get('result', {}).get('mobile_age_info', {}).get('code') == 'SUC':
                age_data = api_data['result']['mobile_age_info'].get('data', {})
                
                MobileAgeInfo.objects.create(
                    mobile_response=mobile_360,
                    code=api_data['result']['mobile_age_info'].get('code', 'NRF'),
                    is_ported=age_data.get('is_ported', ''),
                    mobile_age=age_data.get('mobile_age', ''),
                    number_active=age_data.get('number_active', ''),
                    number_valid=age_data.get('number_valid', ''),
                    ported_region=age_data.get('ported_region', ''),
                    ported_telecom=age_data.get('ported_telecom', ''),
                    region=age_data.get('region', ''),
                    roaming=age_data.get('roaming', ''),
                    telecom=age_data.get('telecom', '')
                )

            # Save WhatsApp Info if available with SUC code
            if api_data.get('result', {}).get('whatsapp_info', {}).get('code') == 'SUC':
                whatsapp_data = api_data['result']['whatsapp_info'].get('data', {})
                
                WhatsappInfo.objects.create(
                    mobile_response=mobile_360,
                    code=api_data['result']['whatsapp_info'].get('code', 'NRF'),
                    status=whatsapp_data.get('status', ''),
                    is_business=whatsapp_data.get('is_business', '')
                )

            # Save Revoke Info if available with SUC code
            if api_data.get('result', {}).get('revoke_info', {}).get('code') == 'SUC':
                revoke_data = api_data['result']['revoke_info'].get('data', {})
                
                RevokeInfo.objects.create(
                    mobile_response=mobile_360,
                    code=api_data['result']['revoke_info'].get('code', 'NRF'),
                    revoke_date=revoke_data.get('revoke_date', ''),
                    revoke_status=revoke_data.get('revoke_status', '')
                )

            # Save Key Highlights
            highlights = api_data.get('result', {}).get('key_highlights', {})
            
            KeyHighlights.objects.create(
                mobile_response=mobile_360,
                digital_payment_id_name=highlights.get('digital_payment_id_name', ''),
                gas_connection_found=highlights.get('gas_connection_found', ''),
                connection_type=highlights.get('connection_type', ''),
                whatsapp_business_account_status=highlights.get('whatsapp_business_account_status', ''),
                age_of_mobile=highlights.get('age_of_mobile', ''),
                active_status=highlights.get('active_status', ''),
                revoke_date=highlights.get('revoke_date', '')
            )

        # Format response for client
        response_data = {
            "mobileNumber": mobile_number,
            "txnId": api_data.get('txnId'),
            "apiCategory": api_data.get('apiCategory'),
            "apiName": api_data.get('apiName'),
            "billable": api_data.get('billable'),
            "message": api_data.get('message'),
            "status": api_data.get('status'),
            "datetime": api_data.get('datetime'),
            "result": api_data.get('result', {})
        }

        return Response(
            create_response(
                status=True,
                message='Data retrieved from API and saved successfully',
                data=response_data
            ), 
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            create_response(
                status=False,
                message=f"Error processing request: {str(e)}",
                data=None
            ), 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def uan_history_search(request):
    try:
        uan_no_list = request.data.get('uanNoList', [])
        realtime_data = request.data.get('realtimeData', False)

        if not uan_no_list:
            return Response(
                create_response(
                    status=False,
                    message='UAN number list is required',
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        response_data = []
        for uan_no in uan_no_list:
            try:
                # Check if data exists in database
                existing_data = None
                if not realtime_data:
                    try:
                        uan_history = UanHistoryLatestV2.objects.get(uan=uan_no)
                        # Construct response from database
                        existing_data = {
                            "uan": uan_no,
                            "txnId": str(uan_history.txn_id),
                            "apiCategory": uan_history.api_category,
                            "apiName": uan_history.api_name,
                            "billable": uan_history.billable,
                            "message": uan_history.message,
                            "status": uan_history.status,
                            "datetime": uan_history.datetime.isoformat(),
                            "result": {
                                "name": uan_history.name,
                                "dob": uan_history.dob.isoformat(),
                                "guardian_name": uan_history.guardian_name,
                                "company_name": uan_history.company_name,
                                "member_id": uan_history.member_id,
                                "date_of_joining": uan_history.date_of_joining.isoformat(),
                                "last_pf_submitted": uan_history.last_pf_submitted.isoformat()
                            }
                        }
                        response_data.append(existing_data)
                        continue
                    except UanHistoryLatestV2.DoesNotExist:
                        pass

                # If no existing data or realtime_data is True, call external API
                api_response = fetch_uan_history_data(uan_no)
                
                if not api_response['success']:
                    response_data.append({
                        "uan": uan_no,
                        "error": api_response['error']
                    })
                    continue
                
                # Get the API response data
                api_data = api_response['data']
                
                try:
                    # Save to database
                    uan_history = UanHistoryLatestV2.objects.create(
                        uan=uan_no,
                        txn_id=api_data['txn_id'],
                        api_category=api_data['api_category'],
                        api_name=api_data['api_name'],
                        billable=api_data['billable'],
                        message=api_data['message'],
                        status=api_data['status'],
                        datetime=datetime.fromisoformat(api_data['datetime']) if isinstance(api_data['datetime'], str) else api_data['datetime'],
                        name=api_data['result']['name'],
                        dob=api_data['result']['dob'],
                        guardian_name=api_data['result']['guardian_name'],
                        company_name=api_data['result']['company_name'],
                        member_id=api_data['result']['member_id'],
                        date_of_joining=api_data['result']['date_of_joining'],
                        last_pf_submitted=api_data['result']['last_pf_submitted']
                    )

                    response_data.append({
                        "uan": uan_no,
                        "txnId": api_data['txn_id'],
                        "apiCategory": api_data['api_category'],
                        "apiName": api_data['api_name'],
                        "billable": api_data['billable'],
                        "message": api_data['message'],
                        "status": api_data['status'],
                        "datetime": api_data['datetime'],
                        "result": api_data['result']
                    })
                except Exception as e:
                    response_data.append({
                        "uan": uan_no,
                        "error": f"Error saving data: {str(e)}"
                    })
            except Exception as e:
                response_data.append({
                    "uan": uan_no,
                    "error": f"Error processing UAN: {str(e)}"
                })

        return Response(
            create_response(
                status=True,
                message='Data retrieved successfully',
                data=response_data
            ), 
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ), 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def uan_employment_history_search(request):
    try:
        uan_no = request.data.get('uanNo')
        realtime_data = request.data.get('realtimeData', False)
        
        if not uan_no:
            return Response(
                create_response(
                    status=False,
                    message='UAN number is required',
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Call external API
        api_response = fetch_uan_employment_data(uan_no)
        
        if not api_response['success']:
            return Response(
                create_response(
                    status=False,
                    message=api_response['error'],
                    data=None
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Get the API response data
        api_data = api_response['data']
        
        try:
            # Save to database with default values if needed
            uan_history = UanEmploymentHistory.objects.create(
                name=api_data['result']['name'] or 'Unknown',
                dob=api_data['result']['dob'] or '01/01/1900'
            )

            # Save company history
            for company_data in api_data['result']['employment_history']:
                CompanyHistory.objects.create(
                    uan_history=uan_history,
                    company_name=company_data.get('company_name', 'Unknown Company'),
                    company_address=company_data.get('company_address', 'Address not available')
                )

            # Format response for client
            response_data = {
                "uan": uan_no,
                "txnId": api_data['txn_id'],
                "apiCategory": api_data['api_category'],
                "apiName": api_data['api_name'],
                "billable": api_data['billable'],
                "message": api_data['message'],
                "status": api_data['status'],
                "datetime": api_data['datetime'],
                "result": {
                    "name": uan_history.name,
                    "dob": uan_history.dob,
                    "employment_history": [
                        {
                            "company_name": history.company_name,
                            "company_address": history.company_address
                        }
                        for history in uan_history.employment_history.all()
                    ]
                }
            }

            return Response(
                create_response(
                    status=True,
                    message='Data retrieved from API and saved successfully',
                    data=response_data
                ), 
                status=status.HTTP_200_OK
            )

        except Exception as e:
            return Response(
                create_response(
                    status=False,
                    message=f"Error saving data: {str(e)}",
                    data=None
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    except Exception as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ), 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def esic_details_search(request):
    try:
        mobile_number = request.data.get('mobileNumber')
        realtime_data = request.data.get('realtimeData', False)

        if not mobile_number:
            return Response(
                create_response(
                    status=False,
                    message='Mobile number is required',
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if data exists in database
        existing_data = None
        if not realtime_data:
            try:
                esic_details = EsicDtls.objects.filter(mobile=mobile_number)
                if esic_details.exists():
                    # Construct response from database
                    existing_data = {
                        "mobileNumber": mobile_number,
                        "result": [
                            {
                                "esic_number": detail.esic_number,
                                "name": detail.name,
                                "employer_code": detail.employer_code,
                                "employer_name": detail.employer_name,
                                "uan_number": detail.uan_number,
                                "bank_details": {
                                    "bank_name": detail.bank_name,
                                    "branch_name": detail.branch_name,
                                    "bank_account_status": detail.bank_account_status
                                }
                            } for detail in esic_details
                        ]
                    }
            except Exception as e:
                pass

        if existing_data and not realtime_data:
            return Response(
                create_response(
                    status=True,
                    message='Data retrieved from database',
                    data=existing_data
                ), 
                status=status.HTTP_200_OK
            )

        # If no existing data or realtime_data is True, call external API
        api_response = fetch_esic_data(mobile_number)
        
        if not api_response['success']:
            return Response(
                create_response(
                    status=False,
                    message=api_response['error'],
                    data=None
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Get the API response data
        api_data = api_response['data']
        
        # Save to database
        esic_details = []
        for esic_record in api_data['result']['esic_details']:
            esic_detail = EsicDtls.objects.create(
                esic_number=esic_record.get('esic_number', ''),
                name=esic_record.get('name', ''),
                employer_code=esic_record.get('employer_code', ''),
                employer_name=esic_record.get('employer_name', ''),
                mobile=mobile_number,
                uan_number=esic_record.get('uan_number', ''),
                bank_name=esic_record.get('bank_name', ''),
                branch_name=esic_record.get('branch_name', ''),
                bank_account_status=esic_record.get('bank_account_status', '')
            )
            esic_details.append(esic_detail)

        # Format response for client
        response_data = {
            "mobileNumber": mobile_number,
            "txnId": api_data.get('txn_id', ''),
            "apiCategory": api_data.get('api_category', ''),
            "apiName": api_data.get('api_name', ''),
            "billable": api_data.get('billable', True),
            "message": api_data.get('message', ''),
            "status": api_data.get('status', 200),
            "datetime": api_data.get('datetime', datetime.now().isoformat()),
            "result": api_data['result']
        }

        return Response(
            create_response(
                status=True,
                message='Data retrieved from API and saved successfully',
                data=response_data
            ), 
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ), 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def gst_advance_v2(request):
    try:
        gstin = request.data.get('gstin')
        realtime_data = request.data.get('realtimeData', False)

        if not gstin:
            return Response(
                create_response(
                    status=False,
                    message='GSTIN is required',
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if data exists in database
        existing_data = None
        if not realtime_data:
            try:
                gst_verification = GstVerification.objects.get(gstin=gstin)
                
                # Construct response from database
                existing_data = {
                    "gstin": gstin,
                    "txnId": request.data.get('txnId', ''),
                    "apiCategory": "KYB",
                    "apiName": "GST Verification (Advance)",
                    "billable": True,
                    "message": "Success",
                    "status": 1,
                    "result": {
                        "aggregate_turn_over": gst_verification.aggregate_turn_over,
                        "authorized_signatory": [
                            signatory.name for signatory in gst_verification.authorized_signatories.all()
                        ],
                        "business_constitution": gst_verification.business_constitution,
                        "business_details": [
                            {
                                "saccd": detail.saccd,
                                "sdes": detail.sdes
                            } for detail in gst_verification.business_details.all()
                        ],
                        "business_nature": [
                            nature.nature for nature in gst_verification.business_natures.all()
                        ],
                        "can_flag": gst_verification.can_flag,
                        "central_jurisdiction": gst_verification.central_jurisdiction,
                        "compliance_rating": gst_verification.compliance_rating,
                        "current_registration_status": gst_verification.current_registration_status,
                        "filing_status": [
                            [
                                {
                                    "fy": status_item.fy,
                                    "taxp": status_item.taxp,
                                    "mof": status_item.mof,
                                    "dof": status_item.dof,
                                    "rtntype": status_item.rtntype,
                                    "arn": status_item.arn,
                                    "status": status_item.status
                                } for status_item in gst_verification.filing_statuses.all()
                            ]
                        ],
                        "gstin": gst_verification.gstin,
                        "is_field_visit_conducted": gst_verification.is_field_visit_conducted,
                        "legal_name": gst_verification.legal_name,
                        "mandate_e_invoice": gst_verification.mandate_e_invoice,
                        "primary_business_address": {
                            "business_nature": gst_verification.primary_address.business_nature,
                            "detailed_address": gst_verification.primary_address.detailed_address,
                            "last_updated_date": gst_verification.primary_address.last_updated_date,
                            "registered_address": gst_verification.primary_address.registered_address
                        } if hasattr(gst_verification, 'primary_address') else {},
                        "register_cancellation_date": gst_verification.register_cancellation_date,
                        "register_date": gst_verification.register_date,
                        "state_jurisdiction": gst_verification.state_jurisdiction,
                        "tax_payer_type": gst_verification.tax_payer_type,
                        "trade_name": gst_verification.trade_name,
                        "gross_total_income": gst_verification.gross_total_income,
                        "gross_total_income_financial_year": gst_verification.gross_total_income_financial_year,
                        "business_email": gst_verification.business_email,
                        "business_mobile": gst_verification.business_mobile
                    }
                }
                
                return Response(
                    create_response(
                        status=True,
                        message='Data retrieved from database',
                        data=existing_data
                    ), 
                    status=status.HTTP_200_OK
                )
                
            except GstVerification.DoesNotExist:
                pass

        # If no existing data or realtime_data is True, call external API
        api_response = fetch_gst_data(gstin)
        
        if not api_response['success']:
            return Response(
                create_response(
                    status=False,
                    message=api_response['error'],
                    data=None
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        # Get the API response data
        api_data = api_response['data']
        result = api_data.get('result', {})
        
        # Save to database
        gst_verification = GstVerification.objects.create(
            gstin=gstin,
            aggregate_turn_over=result.get('aggregate_turn_over', ''),
            business_constitution=result.get('business_constitution', ''),
            can_flag=result.get('can_flag', ''),
            central_jurisdiction=result.get('central_jurisdiction', ''),
            compliance_rating=result.get('compliance_rating', ''),
            current_registration_status=result.get('current_registration_status', ''),
            is_field_visit_conducted=result.get('is_field_visit_conducted', ''),
            legal_name=result.get('legal_name', ''),
            mandate_e_invoice=result.get('mandate_e_invoice', ''),
            register_cancellation_date=result.get('register_cancellation_date', ''),
            register_date=result.get('register_date', ''),
            state_jurisdiction=result.get('state_jurisdiction', ''),
            tax_payer_type=result.get('tax_payer_type', ''),
            trade_name=result.get('trade_name', ''),
            gross_total_income=result.get('gross_total_income', ''),
            gross_total_income_financial_year=result.get('gross_total_income_financial_year', ''),
            business_email=result.get('business_email', ''),
            business_mobile=result.get('business_mobile', '')
        )
        
        # Save authorized signatories
        for signatory_name in result.get('authorized_signatory', []):
            GstAuthorizedSignatory.objects.create(
                gst_verification=gst_verification,
                name=signatory_name
            )
        
        # Save business natures
        for nature in result.get('business_nature', []):
            GstBusinessNature.objects.create(
                gst_verification=gst_verification,
                nature=nature
            )
        
        # Save business details
        for detail in result.get('business_details', []):
            GstBusinessDetail.objects.create(
                gst_verification=gst_verification,
                saccd=detail.get('saccd', ''),
                sdes=detail.get('sdes', '')
            )
        
        # Save filing status
        for filing_group in result.get('filing_status', []):
            for filing in filing_group:
                GstFilingStatus.objects.create(
                    gst_verification=gst_verification,
                    fy=filing.get('fy', ''),
                    taxp=filing.get('taxp', ''),
                    mof=filing.get('mof', ''),
                    dof=filing.get('dof', ''),
                    rtntype=filing.get('rtntype', ''),
                    arn=filing.get('arn', ''),
                    status=filing.get('status', '')
                )
        
        # Save primary business address
        primary_address = result.get('primary_business_address', {})
        if primary_address:
            GstBusinessAddress.objects.create(
                gst_verification=gst_verification,
                business_nature=primary_address.get('business_nature', ''),
                detailed_address=primary_address.get('detailed_address', ''),
                last_updated_date=primary_address.get('last_updated_date', ''),
                registered_address=primary_address.get('registered_address', '')
            )
        
        # Format response for client
        response_data = {
            "gstin": gstin,
            "txnId": api_data.get('txn_id', ''),
            "apiCategory": api_data.get('api_category', 'KYB'),
            "apiName": api_data.get('api_name', 'GST Verification (Advance)'),
            "billable": api_data.get('billable', True),
            "message": api_data.get('message', 'Success'),
            "status": api_data.get('status', 1),
            "result": result
        }

        return Response(
            create_response(
                status=True,
                message='Data retrieved from API and saved successfully',
                data=response_data
            ), 
            status=status.HTTP_200_OK
        )

    except Exception as e:
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ), 
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def gst_turnover(request):
    try:
        gstin = request.data.get('gstin')
        year = request.data.get('year')
        realtime_data = request.data.get('realtimeData', False)

        if not gstin or not year:
            return Response(
                create_response(
                    status=False,
                    message='GSTIN and Year are required',
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Try fetching from DB if not real-time
        if not realtime_data:
            try:
                turnover_data = GstTurnover.objects.filter(gstin=gstin, year=year).order_by('-datetime').first()
                
                if turnover_data:
                    # Get related data
                    authorized_signatories = turnover_data.authorized_signatories.all().values_list('name', flat=True)
                    business_natures = turnover_data.business_natures.all().values_list('nature', flat=True)
                    
                    result = {
                        "gst_estimated_total": turnover_data.gst_estimated_total,
                        "gst_filed_total": turnover_data.gst_filed_total,
                        "year": turnover_data.year,
                        "filing_date": turnover_data.filing_date,
                        "pan_estimated_total": turnover_data.pan_estimated_total,
                        "pan_filed_total": turnover_data.pan_filed_total,
                        "gst_status": turnover_data.gst_status,
                        "legal_name": turnover_data.legal_name,
                        "trade_name": turnover_data.trade_name,
                        "register_date": turnover_data.register_date,
                        "tax_payer_type": turnover_data.tax_payer_type,
                        "authorized_signatory": list(authorized_signatories),
                        "business_nature": list(business_natures)
                    }

                    response_data = {
                        "gstin": gstin,
                        "txnId": turnover_data.txn_id,
                        "apiCategory": "Know Your Business (KYB)",
                        "apiName": "GST Turnover",
                        "billable": True,
                        "message": "Success",
                        "status": 1,
                        "result": result,
                        "datetime": turnover_data.datetime.strftime("%Y-%m-%d %H:%M:%S.%f")
                    }

                    return Response(
                        create_response(
                            status=True,
                            message='Data retrieved from database',
                            data=response_data
                        ),
                        status=status.HTTP_200_OK
                    )

            except Exception as db_error:
                logger.error(f"Error retrieving from database: {str(db_error)}")
                # Continue to API call if there's an error retrieving from DB

        # Call external API
        api_response = fetch_gst_turnover_data(gstin, year)

        if not api_response['success']:
            return Response(
                create_response(
                    status=False,
                    message=api_response['error'],
                    data=None
                ),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        api_data = api_response['data']
        
        # Check for API response status
        api_status = api_data.get('status')
        if api_status != 1:  # Status 1 typically means success
            # Return the API's error response directly
            return Response(
                create_response(
                    status=False,
                    message=api_data.get('message', 'External API returned an error'),
                    data=api_data
                ),
                status=status.HTTP_400_BAD_REQUEST
            )
            
        result = api_data.get('result', {})
        
        # Current datetime for the record
        current_datetime = timezone.now()
        
        # Create the GST Turnover record with all required fields
        try:
            turnover_record = GstTurnover.objects.create(
                txn_id=api_data.get('txn_id', str(uuid.uuid4())),
                gstin=gstin,
                gst_estimated_total=result.get('gst_estimated_total'),
                gst_filed_total=result.get('gst_filed_total', 0),
                year=result.get('year', year),
                filing_date=result.get('filing_date', ''),
                pan_estimated_total=result.get('pan_estimated_total', 0),
                pan_filed_total=result.get('pan_filed_total', 0),
                gst_status=result.get('gst_status', ''),
                legal_name=result.get('legal_name', ''),
                trade_name=result.get('trade_name', ''),
                register_date=result.get('register_date', ''),
                tax_payer_type=result.get('tax_payer_type', ''),
                datetime=datetime.strptime(api_data.get('datetime', current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")), 
                                           "%Y-%m-%d %H:%M:%S.%f"),
                turnover=result.get('gst_filed_total', 0),
                source='API',
                last_updated=current_datetime
            )
            
            # Save the authorized signatories
            for signatory in result.get('authorized_signatory', []):
                GstTurnoverAuthorizedSignatory.objects.create(
                    gst_turnover=turnover_record,
                    name=signatory
                )
                
            # Save the business natures
            for nature in result.get('business_nature', []):
                GstTurnoverBusinessNature.objects.create(
                    gst_turnover=turnover_record,
                    nature=nature
                )
            
            # Prepare response - use the actual API data to ensure accuracy
            response_data = {
                "gstin": gstin,
                "txnId": api_data.get('txn_id', ''),
                "apiCategory": api_data.get('api_category', 'Know Your Business (KYB)'),
                "apiName": api_data.get('api_name', 'GST Turnover'),
                "billable": api_data.get('billable', True),
                "message": api_data.get('message', 'Success'),
                "status": api_data.get('status', 1),
                "result": result,  # Use the original result directly
                "datetime": api_data.get('datetime', current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f"))
            }

            return Response(
                create_response(
                    status=True,
                    message='Data retrieved from API and saved successfully',
                    data=response_data
                ),
                status=status.HTTP_200_OK
            )
            
        except Exception as db_error:
            logger.error(f"Database error: {str(db_error)}")
            # If we can't save to the database, still return the API response to the user
            response_data = {
                "gstin": gstin,
                "txnId": api_data.get('txn_id', ''),
                "apiCategory": api_data.get('api_category', 'Know Your Business (KYB)'),
                "apiName": api_data.get('api_name', 'GST Turnover'),
                "billable": api_data.get('billable', True),
                "message": api_data.get('message', 'Success'),
                "status": api_data.get('status', 1),
                "result": result,
                "datetime": api_data.get('datetime', current_datetime.strftime("%Y-%m-%d %H:%M:%S.%f")),
                "db_error": str(db_error)  # Add the error for debugging
            }
            
            return Response(
                create_response(
                    status=True,
                    message='Data retrieved from API but failed to save to database',
                    data=response_data
                ),
                status=status.HTTP_200_OK
            )

    except Exception as e:
        logger.error(f"General error in gst_turnover view: {str(e)}")
        return Response(
            create_response(
                status=False,
                message=str(e),
                data=None
            ),
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

@api_view(['POST'])
def udyam_details_search(request):
    try:
        udyam_number = request.data.get('registration_no')
        realtime = request.data.get('realtimeData', False)

        if not udyam_number:
            return Response(create_response(False, 'Udyam number is required', None), status=status.HTTP_400_BAD_REQUEST)

        # If not realtime, check DB first
        if not realtime:
            try:
                existing = UdyamDetails.objects.filter(udyamnumber=udyam_number).first()
                
                if existing:
                    return Response(create_response(True, 'Data retrieved from database', {
                        'udyam_number': udyam_number,  # Use the input instead
                        'enterprise_name': existing.enterprise_name,
                        'organisation_type': existing.organisation_type,
                        # Add more fields as needed
                    }), status=status.HTTP_200_OK)
            except Exception as db_err:
                # Return error message instead of print
                return Response(create_response(False, f"Database error: {str(db_err)}", None), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Realtime fetch
        api_response = fetch_udyam_data(udyam_number)

        if not api_response['success']:
            return Response(create_response(False, api_response['error'], None), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = api_response['data']

        # If API returns Source Down or only header info, save only that
        result = data.get('result')
        if not result:
            try:
                # Try to create or update, but allow it to fail gracefully
                # Skip the udyamnumber field for now if it's causing issues
                obj, created = UdyamDetails.objects.update_or_create(
                    # Use a different unique identifier temporarily
                    txn_id=data['txn_id'],
                    defaults={
                        # Skip udyamnumber if causing issues
                        # 'udyamnumber': udyam_number,
                        'api_category': data['api_category'],
                        'api_name': data['api_name'],
                        'billable': data['billable'],
                        'message': data['message'],
                        'status': data['status'],
                        'datetime': data['datetime'],
                        'enterprise_name': '',
                        'organisation_type': '',
                        'service_type': '',
                        'gender': '',
                        'social_category': '',
                        'date_of_incorporation': '1900-01-01',
                        'date_of_commencement': '1900-01-01',
                        'mobile': '',
                        'email': '',
                        'dic': '',
                        'msme_dfo': '',
                        'date_of_udyam_registeration': '1900-01-01',
                    }
                )
            except Exception as e:
                return Response(create_response(False, f"Failed to save metadata: {str(e)}", None), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
            return Response(create_response(True, 'Only metadata received (e.g. source down)', data), status=status.HTTP_200_OK)

        # Clean fields for nested saving
        address = result.pop('address', {})
        plants = result.pop('plant_details', [])
        types = result.pop('enterprise_type', [])
        nics = result.pop('nic_code', [])

        try:
            # Try to delete if exists, but don't fail if it doesn't
            UdyamDetails.objects.filter(txn_id=data['txn_id']).delete()  # Use txn_id as a temporary workaround
        except Exception as e:
            return Response(create_response(False, f"Error deleting old records: {str(e)}", None), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Prepare flat fields from result
        field_data = {k: v for k, v in result.items() if hasattr(UdyamDetails, k)}

        try:
            # Create a new record with all fields except udyamnumber if that's causing issues
            udyam = UdyamDetails(
                # Skip udyamnumber if causing issues
                # udyamnumber=udyam_number,
                txn_id=data['txn_id'],
                api_category=data['api_category'],
                api_name=data['api_name'],
                billable=data['billable'],
                message=data['message'],
                status=data['status'],
                datetime=data['datetime'],
                **field_data
            )
            udyam.save()
            
            # If you can add the udyamnumber after saving
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute(
                        "UPDATE udyam_details SET udyamnumber = %s WHERE id = %s", 
                        [udyam_number, udyam.id]
                    )
            except Exception as e:
                return Response(create_response(False, f"Failed to update udyamnumber: {str(e)}", None), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            # Save nested models
            if address:
                UdyamAddress.objects.create(udyam=udyam, **address)

            for plant in plants:
                UdyamPlantDetail.objects.create(udyam=udyam, **plant)

            for et in types:
                et['classification_date'] = datetime.strptime(et['classification_date'], '%d/%m/%Y').date()
                UdyamEnterpriseType.objects.create(udyam=udyam, **et)

            for nic in nics:
                nic['date'] = datetime.strptime(nic['date'], '%d/%m/%Y').date()
                UdyamNICCode.objects.create(udyam=udyam, **nic)
                
        except Exception as e:
            # Return error message instead of print
            return Response(create_response(False, f"Failed to save main data: {str(e)}", None), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(create_response(True, 'Realtime data retrieved and saved successfully', data), status=status.HTTP_200_OK)

    except Exception as e:
        return Response(create_response(False, str(e), None), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
@api_view(['POST'])
def mobile_to_account_search(request):
    try:
        mobile = request.data.get('mobile')
        realtime = request.data.get('realtimeData', False)

        if not mobile:
            return Response(create_response(False, 'Mobile number is required', None), status=status.HTTP_400_BAD_REQUEST)

        # Check if data exists in database
        existing_record = None
        
        try:
            existing_record = MobileToAccountDetails.objects.get(mobile=mobile)
            
            # If not requesting realtime data, return existing data
            if not realtime:
                # Format the response to match the realtime data format
                formatted_response = {
                    "mobile": mobile,
                    "txn_id": str(existing_record.txn_id),
                    "api_category": existing_record.api_category,
                    "api_name": existing_record.api_name,
                    "billable": existing_record.billable,
                    "message": existing_record.message,
                    "status": existing_record.status,
                    "datetime": existing_record.datetime.isoformat(),
                    "result": {
                        "account_details": {
                            "account_ifsc": existing_record.account_details.account_ifsc,
                            "account_number": existing_record.account_details.account_number,
                            "amount_deposited": str(existing_record.account_details.amount_deposited)
                        },
                        "vpa_details": {
                            "account_holder_name": existing_record.vpa_details.account_holder_name,
                            "vpa": existing_record.vpa_details.vpa
                        }
                    }
                }
                
                return Response(create_response(True, 'Data from database', formatted_response), status=status.HTTP_200_OK)
        except MobileToAccountDetails.DoesNotExist:
            existing_record = None

        # Call external API if no existing data or realtime_data is True
        api_response = fetch_mobile_to_account_data(mobile)
        if not api_response['success']:
            return Response(create_response(False, api_response['error'], None), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        data = api_response['data']
        
        # Validate that the required fields exist in the API response
        if 'result' not in data:
            return Response(create_response(False, 'Invalid API response: missing result field', None), 
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        result = data.get('result', {})
        
        # Check if account_details and vpa_details exist
        if 'account_details' not in result or 'vpa_details' not in result:
            return Response(create_response(False, 'Invalid API response: missing account or VPA details', None), 
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        acc = result.get('account_details', {})
        vpa = result.get('vpa_details', {})
        
        # Validate required fields for database creation
        required_fields = ['txn_id', 'api_category', 'api_name', 'billable', 'message', 'status', 'datetime']
        missing_fields = [field for field in required_fields if field not in data]
        
        if missing_fields:
            return Response(create_response(False, f'Invalid API response: missing fields {missing_fields}', None), 
                           status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Transaction handling for database operations
        with transaction.atomic():
            # If record exists, update it instead of creating a new one
            if existing_record:
                # Update the main MobileToAccountDetails record
                existing_record.txn_id = data.get('txn_id')
                existing_record.api_category = data.get('api_category', '')
                existing_record.api_name = data.get('api_name', '')
                existing_record.billable = data.get('billable', False)
                existing_record.message = data.get('message', '')
                existing_record.status = data.get('status', 0)
                existing_record.datetime = data.get('datetime')
                existing_record.save()
                
                record = existing_record
                
                # Update related records
                # Validate required fields for AccountDetails
                required_acc_fields = ['account_ifsc', 'account_number', 'amount_deposited']
                missing_acc_fields = [field for field in required_acc_fields if field not in acc]
                
                if missing_acc_fields:
                    return Response(create_response(False, f'Invalid API response: missing account fields {missing_acc_fields}', None), 
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Update AccountDetails
                account_details = record.account_details
                account_details.account_ifsc = acc['account_ifsc']
                account_details.account_number = acc['account_number']
                account_details.amount_deposited = acc['amount_deposited']
                account_details.save()
                
                # Validate required fields for VpaDetails
                required_vpa_fields = ['account_holder_name', 'vpa']
                missing_vpa_fields = [field for field in required_vpa_fields if field not in vpa]
                
                if missing_vpa_fields:
                    return Response(create_response(False, f'Invalid API response: missing VPA fields {missing_vpa_fields}', None), 
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # Update VpaDetails
                vpa_details = record.vpa_details
                vpa_details.account_holder_name = vpa['account_holder_name']
                vpa_details.vpa = vpa['vpa']
                vpa_details.save()
            else:
                # Create new record if it doesn't exist
                record = MobileToAccountDetails.objects.create(
                    txn_id=data['txn_id'],
                    api_category=data['api_category'],
                    api_name=data['api_name'],
                    billable=data['billable'],
                    message=data['message'],
                    status=data['status'],
                    datetime=data['datetime'],
                    mobile=mobile
                )
                
                # Validate required fields for AccountDetails
                required_acc_fields = ['account_ifsc', 'account_number', 'amount_deposited']
                missing_acc_fields = [field for field in required_acc_fields if field not in acc]
                
                if missing_acc_fields:
                    # Clean up the record we just created since we can't complete the process
                    record.delete()
                    return Response(create_response(False, f'Invalid API response: missing account fields {missing_acc_fields}', None), 
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                AccountDetails.objects.create(
                    record=record,
                    account_ifsc=acc['account_ifsc'],
                    account_number=acc['account_number'],
                    amount_deposited=acc['amount_deposited'],
                )
                
                # Validate required fields for VpaDetails
                required_vpa_fields = ['account_holder_name', 'vpa']
                missing_vpa_fields = [field for field in required_vpa_fields if field not in vpa]
                
                if missing_vpa_fields:
                    # Clean up the records we just created since we can't complete the process
                    record.delete()  # This will cascade delete the AccountDetails too
                    return Response(create_response(False, f'Invalid API response: missing VPA fields {missing_vpa_fields}', None), 
                                  status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                VpaDetails.objects.create(
                    record=record,
                    account_holder_name=vpa['account_holder_name'],
                    vpa=vpa['vpa'],
                )

        # Return the API response directly to maintain the same format
        return Response(create_response(True, 'Data retrieved and saved successfully', data), status=status.HTTP_200_OK)

    except Exception as e:
        return Response(create_response(False, f'Error processing request: {str(e)}', None), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    