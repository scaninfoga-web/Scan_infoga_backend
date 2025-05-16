from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from core.utils import create_response

from .models import (
    Mobile360, DigitalPaymentInfo, LPGInfo, TelcoInfo,
    MobileAgeInfo, WhatsappInfo, RevokeInfo, KeyHighlights,
    UanHistoryLatestV2,UanEmploymentHistory, GstVerification, EsicDtls
)
from .utils import fetch_mobile360_data, fetch_uan_employment_data, fetch_uan_history_data,fetch_esic_data,fetch_gst_data

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

        # In mobile_360_search function, update the API response handling:
        
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