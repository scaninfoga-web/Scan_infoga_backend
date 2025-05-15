from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
import uuid
import json

from .models import (
    Mobile360, DigitalPaymentInfo, LPGInfo, TelcoInfo,
    MobileAgeInfo, WhatsappInfo, RevokeInfo, KeyHighlights
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
                        "digitalPaymentIdInfo": {
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
                        "lpgInfo": {
                            "code": "SUC" if mobile_360.lpg_info.exists() else "NRF",
                            "data": [{
                                "gasProvider": lpg.gas_provider,
                                "name": lpg.name,
                                "consumerDetails": {
                                    "consumerMobile": lpg.consumer_mobile,
                                    "consumerId": lpg.consumer_id,
                                    "consumerStatus": lpg.consumer_status,
                                    "consumerType": lpg.consumer_type
                                },
                                "address": lpg.address,
                                "distributorDetails": {
                                    "distributorCode": lpg.distributor_code,
                                    "distributorName": lpg.distributor_name,
                                    "distributorContact": lpg.distributor_contact,
                                    "distributorAddress": lpg.distributor_address
                                }
                            } for lpg in mobile_360.lpg_info.all()]
                        },
                        "telcoInfo": {
                            "code": mobile_360.telco_info.code if hasattr(mobile_360, 'telco_info') else "NRF",
                            "data": {
                                "isValid": mobile_360.telco_info.is_valid,
                                "subscriberStatus": mobile_360.telco_info.subscriber_status,
                                "connectionType": mobile_360.telco_info.connection_type,
                                "msisdn": {
                                    "msisdn": mobile_360.telco_info.msisdn,
                                    "msisdnCountryCode": mobile_360.telco_info.msisdn_country_code
                                },
                                "currentServiceProvider": {
                                    "networkName": mobile_360.telco_info.network_name,
                                    "networkRegion": mobile_360.telco_info.network_region
                                },
                                "isRoaming": mobile_360.telco_info.is_roaming
                            } if hasattr(mobile_360, 'telco_info') else {}
                        },
                        "mobileAgeInfo": {
                            "code": mobile_360.mobile_age_info.code if hasattr(mobile_360, 'mobile_age_info') else "NRF",
                            "data": {
                                "isPorted": mobile_360.mobile_age_info.is_ported,
                                "mobileAge": mobile_360.mobile_age_info.mobile_age,
                                "numberActive": mobile_360.mobile_age_info.number_active,
                                "numberValid": mobile_360.mobile_age_info.number_valid,
                                "portedRegion": mobile_360.mobile_age_info.ported_region,
                                "portedTelecom": mobile_360.mobile_age_info.ported_telecom,
                                "region": mobile_360.mobile_age_info.region,
                                "roaming": mobile_360.mobile_age_info.roaming,
                                "telecom": mobile_360.mobile_age_info.telecom
                            } if hasattr(mobile_360, 'mobile_age_info') else {}
                        },
                        "whatsappInfo": {
                            "code": mobile_360.whatsapp_info.code if hasattr(mobile_360, 'whatsapp_info') else "NRF",
                            "data": {
                                "status": mobile_360.whatsapp_info.status,
                                "isBusiness": mobile_360.whatsapp_info.is_business
                            } if hasattr(mobile_360, 'whatsapp_info') else {}
                        },
                        "revokeInfo": {
                            "code": mobile_360.revoke_info.code if hasattr(mobile_360, 'revoke_info') else "NRF",
                            "data": {
                                "revokeDate": mobile_360.revoke_info.revoke_date,
                                "revokeStatus": mobile_360.revoke_info.revoke_status
                            } if hasattr(mobile_360, 'revoke_info') else {}
                        },
                        "keyHighlights": {
                            "digitalPaymentIdName": mobile_360.key_highlights.digital_payment_id_name if hasattr(mobile_360, 'key_highlights') else "",
                            "gasConnectionFound": mobile_360.key_highlights.gas_connection_found if hasattr(mobile_360, 'key_highlights') else "",
                            "connectionType": mobile_360.key_highlights.connection_type if hasattr(mobile_360, 'key_highlights') else "",
                            "whatsappBusinessAccountStatus": mobile_360.key_highlights.whatsapp_business_account_status if hasattr(mobile_360, 'key_highlights') else "",
                            "ageOfMobile": mobile_360.key_highlights.age_of_mobile if hasattr(mobile_360, 'key_highlights') else "",
                            "activeStatus": mobile_360.key_highlights.active_status if hasattr(mobile_360, 'key_highlights') else "",
                            "revokeDate": mobile_360.key_highlights.revoke_date if hasattr(mobile_360, 'key_highlights') else ""
                        }
                    }
                }

            except Mobile360.DoesNotExist:
                pass

        if existing_data and not realtime_data:
            return Response({
                'status': True,
                'message': 'Data retrieved from database',
                'data': existing_data
            }, status=status.HTTP_200_OK)

        # If no existing data or realtime_data is True, call external API
        mock_response = {
            "mobile_number": mobile_number,
            "txn_id": str(uuid.uuid4()),
            "api_category": "Fraud Check",
            "api_name": "Mobile 360",
            "billable": True,
            "message": "Success",
            "status": 1,
            "datetime": datetime.now().isoformat(),
            "result": {
                "digital_payment_id_info": {
                    "code": "SUC",
                    "data": {
                        "name": "Apoorva Somani",
                        "bank": "State Bank of India",
                        "branch": "CYBER TREASURY, DEHRADUN",
                        "center": "",
                        "district": "DEHRADUN",
                        "state": "UTTARAKHAND",
                        "address": "23 LAXMI ROAD, DALANWALA, DEHRADUN.UTTARAKHAND248001",
                        "contact": "",
                        "city": "DEHRADUN"
                    }
                },
                # ... simulate other response data ...
            }
        }

        # Save to database
        mobile_360 = Mobile360.objects.create(
            mobile_number=mobile_number,
            txn_id=mock_response['txn_id'],
            api_category=mock_response['api_category'],
            api_name=mock_response['api_name'],
            billable=mock_response['billable'],
            message=mock_response['message'],
            status=mock_response['status'],
            datetime=mock_response['datetime']
        )

        # Save Digital Payment Info
        if mock_response['result']['digital_payment_id_info']['code'] == 'SUC':
            payment_data = mock_response['result']['digital_payment_id_info']['data']
            DigitalPaymentInfo.objects.create(
                mobile_response=mobile_360,
                code=mock_response['result']['digital_payment_id_info']['code'],
                name=payment_data['name'],
                bank=payment_data['bank'],
                branch=payment_data['branch'],
                center=payment_data['center'],
                district=payment_data['district'],
                state=payment_data['state'],
                address=payment_data['address'],
                contact=payment_data['contact'],
                city=payment_data['city']
            )

        # Save LPG Info
        if mock_response['result'].get('lpg_info', {}).get('code') == 'SUC':
            for lpg_data in mock_response['result']['lpg_info']['data']:
                LPGInfo.objects.create(
                    mobile_response=mobile_360,
                    code=mock_response['result']['lpg_info']['code'],
                    gas_provider=lpg_data['gas_provider'],
                    name=lpg_data['name'],
                    consumer_mobile=lpg_data['consumer_details']['consumer_mobile'],
                    consumer_id=lpg_data['consumer_details']['consumer_id'],
                    consumer_status=lpg_data['consumer_details']['consumer_status'],
                    consumer_type=lpg_data['consumer_details']['consumer_type'],
                    address=lpg_data['address'],
                    distributor_code=lpg_data['distributor_details']['distributor_code'],
                    distributor_name=lpg_data['distributor_details']['distributor_name'],
                    distributor_contact=lpg_data['distributor_details']['distributor_contact'],
                    distributor_address=lpg_data['distributor_details']['distributor_address']
                )

        # Save Telco Info
        if mock_response['result'].get('telco_info', {}).get('code') == 'SUC':
            telco_data = mock_response['result']['telco_info']['data']
            TelcoInfo.objects.create(
                mobile_response=mobile_360,
                code=mock_response['result']['telco_info']['code'],
                is_valid=telco_data['is_valid'],
                subscriber_status=telco_data['subscriber_status'],
                connection_type=telco_data['connection_type'],
                msisdn=telco_data['msisdn']['msisdn'],
                msisdn_country_code=telco_data['msisdn']['msisdn_country_code'],
                network_name=telco_data['current_service_provider']['network_name'],
                network_region=telco_data['current_service_provider']['network_region'],
                is_roaming=telco_data['is_roaming']
            )

        # Save Mobile Age Info
        if mock_response['result'].get('mobile_age_info', {}).get('code') == 'SUC':
            age_data = mock_response['result']['mobile_age_info']['data']
            MobileAgeInfo.objects.create(
                mobile_response=mobile_360,
                code=mock_response['result']['mobile_age_info']['code'],
                is_ported=age_data['is_ported'],
                mobile_age=age_data['mobile_age'],
                number_active=age_data['number_active'],
                number_valid=age_data['number_valid'],
                ported_region=age_data['ported_region'],
                ported_telecom=age_data['ported_telecom'],
                region=age_data['region'],
                roaming=age_data['roaming'],
                telecom=age_data['telecom']
            )

        # Save WhatsApp Info
        if mock_response['result'].get('whatsapp_info', {}).get('code') == 'SUC':
            whatsapp_data = mock_response['result']['whatsapp_info']['data']
            WhatsappInfo.objects.create(
                mobile_response=mobile_360,
                code=mock_response['result']['whatsapp_info']['code'],
                status=whatsapp_data['status'],
                is_business=whatsapp_data['is_business']
            )

        # Save Revoke Info
        if mock_response['result'].get('revoke_info', {}).get('code') == 'SUC':
            revoke_data = mock_response['result']['revoke_info']['data']
            RevokeInfo.objects.create(
                mobile_response=mobile_360,
                code=mock_response['result']['revoke_info']['code'],
                revoke_date=revoke_data['revoke_date'],
                revoke_status=revoke_data['revoke_status']
            )

        # Save Key Highlights
        highlights = mock_response['result']['key_highlights']
        KeyHighlights.objects.create(
            mobile_response=mobile_360,
            digital_payment_id_name=highlights['digital_payment_id_name'],
            gas_connection_found=highlights['gas_connection_found'],
            connection_type=highlights['connection_type'],
            whatsapp_business_account_status=highlights['whatsapp_business_account_status'],
            age_of_mobile=highlights['age_of_mobile'],
            active_status=highlights['active_status'],
            revoke_date=highlights['revoke_date']
        )

        return Response({
            'status': True,
            'message': 'Data saved successfully',
            'data': mock_response
        }, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({
            'status': False,
            'message': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
