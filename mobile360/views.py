from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from core.utils import create_response

from .models import (
    Mobile360, DigitalPaymentInfo, LPGInfo, TelcoInfo,
    MobileAgeInfo, WhatsappInfo, RevokeInfo, KeyHighlights
)
from .utils import fetch_mobile360_data, fetch_uan_employment_data, fetch_uan_history_data

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
        if not realtime_data:
            try:
                mobile_360 = Mobile360.objects.get(mobile_number=mobile_number)
                # Construct response from database
                existing_data = {
                    "mobileNumber": mobile_number,
                    "txnId": str(mobile_360.txn_id),
                    "apiCategory": mobile_360.api_category,
                    "apiName": mobile_360.api_name,
                    "billable": mobile_360.billable,
                    "message": mobile_360.message,
                    "status": mobile_360.status,
                    "datetime": mobile_360.datetime.isoformat(),
                    "result": {
                        "digital_payment_id_info": {
                            "code": mobile_360.digital_payment_info.code if hasattr(mobile_360, 'digital_payment_info') else "NRF",
                            "data": {
                                "name": mobile_360.digital_payment_info.name,
                                "bank": mobile_360.digital_payment_info.bank,
                                "branch": mobile_360.digital_payment_info.branch,
                                "center": mobile_360.digital_payment_info.center,
                                "district": mobile_360.digital_payment_info.district,
                                "state": mobile_360.digital_payment_info.state,
                                "address": mobile_360.digital_payment_info.address,
                                "contact": mobile_360.digital_payment_info.contact,
                                "city": mobile_360.digital_payment_info.city
                            } if hasattr(mobile_360, 'digital_payment_info') else {}
                        },
                        "lpg_info": {
                            "code": "SUC" if mobile_360.lpg_info.exists() else "NRF",
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
                            } for lpg in mobile_360.lpg_info.all()]
                        },
                        "telco_info": {
                            "code": mobile_360.telco_info.code if hasattr(mobile_360, 'telco_info') else "NRF",
                            "data": {
                                "is_valid": mobile_360.telco_info.is_valid,
                                "subscriber_status": mobile_360.telco_info.subscriber_status,
                                "connection_type": mobile_360.telco_info.connection_type,
                                "msisdn": {
                                    "msisdn": mobile_360.telco_info.msisdn,
                                    "msisdn_country_code": mobile_360.telco_info.msisdn_country_code
                                },
                                "current_service_provider": {
                                    "network_name": mobile_360.telco_info.network_name,
                                    "network_region": mobile_360.telco_info.network_region
                                },
                                "is_roaming": mobile_360.telco_info.is_roaming
                            } if hasattr(mobile_360, 'telco_info') else {}
                        },
                        "mobile_age_info": {
                            "code": mobile_360.mobile_age_info.code if hasattr(mobile_360, 'mobile_age_info') else "NRF",
                            "data": {
                                "is_ported": mobile_360.mobile_age_info.is_ported,
                                "mobile_age": mobile_360.mobile_age_info.mobile_age,
                                "number_active": mobile_360.mobile_age_info.number_active,
                                "number_valid": mobile_360.mobile_age_info.number_valid,
                                "ported_region": mobile_360.mobile_age_info.ported_region,
                                "ported_telecom": mobile_360.mobile_age_info.ported_telecom,
                                "region": mobile_360.mobile_age_info.region,
                                "roaming": mobile_360.mobile_age_info.roaming,
                                "telecom": mobile_360.mobile_age_info.telecom
                            } if hasattr(mobile_360, 'mobile_age_info') else {}
                        },
                        "whatsapp_info": {
                            "code": mobile_360.whatsapp_info.code if hasattr(mobile_360, 'whatsapp_info') else "NRF",
                            "data": {
                                "status": mobile_360.whatsapp_info.status,
                                "is_business": mobile_360.whatsapp_info.is_business
                            } if hasattr(mobile_360, 'whatsapp_info') else {}
                        },
                        "revoke_info": {
                            "code": mobile_360.revoke_info.code if hasattr(mobile_360, 'revoke_info') else "NRF",
                            "data": {
                                "revoke_date": mobile_360.revoke_info.revoke_date,
                                "revoke_status": mobile_360.revoke_info.revoke_status
                            } if hasattr(mobile_360, 'revoke_info') else {}
                        },
                        "key_highlights": {
                            "digital_payment_id_name": mobile_360.key_highlights.digital_payment_id_name if hasattr(mobile_360, 'key_highlights') else "",
                            "gas_connection_found": mobile_360.key_highlights.gas_connection_found if hasattr(mobile_360, 'key_highlights') else "",
                            "connection_type": mobile_360.key_highlights.connection_type if hasattr(mobile_360, 'key_highlights') else "",
                            "whatsapp_business_account_status": mobile_360.key_highlights.whatsapp_business_account_status if hasattr(mobile_360, 'key_highlights') else "",
                            "age_of_mobile": mobile_360.key_highlights.age_of_mobile if hasattr(mobile_360, 'key_highlights') else "",
                            "active_status": mobile_360.key_highlights.active_status if hasattr(mobile_360, 'key_highlights') else "",
                            "revoke_date": mobile_360.key_highlights.revoke_date if hasattr(mobile_360, 'key_highlights') else ""
                        }
                    }
                }

            except Mobile360.DoesNotExist:
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
        api_response = fetch_mobile360_data(mobile_number)
        
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
        mobile_360 = Mobile360.objects.create(
            mobile_number=mobile_number,
            txn_id=api_data['txn_id'],
            api_category=api_data['api_category'],
            api_name=api_data['api_name'],
            billable=api_data['billable'],
            message=api_data['message'],
            status=api_data['status'],
            datetime=datetime.fromisoformat(api_data['datetime']) if isinstance(api_data['datetime'], str) else api_data['datetime']
        )

        # Save Digital Payment Info
        if api_data['result']['digital_payment_id_info']['code'] == 'SUC':
            payment_data = api_data['result']['digital_payment_id_info']['data']
            DigitalPaymentInfo.objects.create(
                mobile_response=mobile_360,
                code=api_data['result']['digital_payment_id_info']['code'],
                name=payment_data.get('name'),
                bank=payment_data.get('bank'),
                branch=payment_data.get('branch'),
                center=payment_data.get('center', ''),
                district=payment_data.get('district'),
                state=payment_data.get('state'),
                address=payment_data.get('address'),
                contact=payment_data.get('contact', ''),
                city=payment_data.get('city')
            )

        # Save LPG Info
        if api_data['result'].get('lpg_info', {}).get('code') == 'SUC':
            for lpg_data in api_data['result']['lpg_info']['data']:
                LPGInfo.objects.create(
                    mobile_response=mobile_360,
                    code=api_data['result']['lpg_info']['code'],
                    gas_provider=lpg_data.get('gas_provider'),
                    name=lpg_data.get('name'),
                    consumer_mobile=lpg_data.get('consumer_details', {}).get('consumer_mobile'),
                    consumer_id=lpg_data.get('consumer_details', {}).get('consumer_id'),
                    consumer_status=lpg_data.get('consumer_details', {}).get('consumer_status'),
                    consumer_type=lpg_data.get('consumer_details', {}).get('consumer_type'),
                    address=lpg_data.get('address'),
                    distributor_code=lpg_data.get('distributor_details', {}).get('distributor_code'),
                    distributor_name=lpg_data.get('distributor_details', {}).get('distributor_name'),
                    distributor_contact=lpg_data.get('distributor_details', {}).get('distributor_contact'),
                    distributor_address=lpg_data.get('distributor_details', {}).get('distributor_address')
                )

        # Save Telco Info
        if api_data['result'].get('telco_info', {}).get('code') == 'SUC':
            telco_data = api_data['result']['telco_info']['data']
            TelcoInfo.objects.create(
                mobile_response=mobile_360,
                code=api_data['result']['telco_info']['code'],
                is_valid=telco_data.get('is_valid'),
                subscriber_status=telco_data.get('subscriber_status'),
                connection_type=telco_data.get('connection_type'),
                msisdn=telco_data.get('msisdn', {}).get('msisdn'),
                msisdn_country_code=telco_data.get('msisdn', {}).get('msisdn_country_code'),
                network_name=telco_data.get('current_service_provider', {}).get('network_name'),
                network_region=telco_data.get('current_service_provider', {}).get('network_region'),
                is_roaming=telco_data.get('is_roaming')
            )

        # Save Mobile Age Info
        if api_data['result'].get('mobile_age_info', {}).get('code') == 'SUC':
            age_data = api_data['result']['mobile_age_info']['data']
            MobileAgeInfo.objects.create(
                mobile_response=mobile_360,
                code=api_data['result']['mobile_age_info']['code'],
                is_ported=age_data.get('is_ported'),
                mobile_age=age_data.get('mobile_age'),
                number_active=age_data.get('number_active'),
                number_valid=age_data.get('number_valid'),
                ported_region=age_data.get('ported_region', ''),
                ported_telecom=age_data.get('ported_telecom', ''),
                region=age_data.get('region'),
                roaming=age_data.get('roaming'),
                telecom=age_data.get('telecom')
            )

        # Save WhatsApp Info
        if api_data['result'].get('whatsapp_info', {}).get('code') == 'SUC':
            whatsapp_data = api_data['result']['whatsapp_info']['data']
            WhatsappInfo.objects.create(
                mobile_response=mobile_360,
                code=api_data['result']['whatsapp_info']['code'],
                status=whatsapp_data.get('status'),
                is_business=whatsapp_data.get('is_business')
            )

        # Save Revoke Info
        if api_data['result'].get('revoke_info', {}).get('code') == 'SUC':
            revoke_data = api_data['result']['revoke_info']['data']
            RevokeInfo.objects.create(
                mobile_response=mobile_360,
                code=api_data['result']['revoke_info']['code'],
                revoke_date=revoke_data.get('revoke_date', ''),
                revoke_status=revoke_data.get('revoke_status')
            )

        # Save Key Highlights
        highlights = api_data['result'].get('key_highlights', {})
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
            "txnId": api_data['txn_id'],
            "apiCategory": api_data['api_category'],
            "apiName": api_data['api_name'],
            "billable": api_data['billable'],
            "message": api_data['message'],
            "status": api_data['status'],
            "datetime": api_data['datetime'],
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


####################### UAN HISTORY ####################

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

####################### UAN EMPLOYMENT HISTORY 
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
            except UanHistoryLatestV2.DoesNotExist:
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