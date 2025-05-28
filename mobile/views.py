# views.py
from venv import create
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
import requests
import json

from core.utils import create_response

from .models import (
    Mobile360Report,
    UANHistoryReport, 
    UANEmploymentReport,
    ESICReport,
    GSTVerificationReport, 
    GSTTurnoverReport, 
    UdyamReport, 
    ProfileAdvanceReport, 
    EquifaxV3Report,
    MobileToDLLookup,
    MobileToAccountNumber,
    UanWithoutOtp,
    PanAllInOne,
    DigitalPaymentAnalyser
)


from .serializers import (
    Mobile360ReportSerializer, 
    UANHistoryReportSerializer, 
    UANEmploymentReportSerializer, 
    ESICReportSerializer, 
    GSTVerificationReportSerializer, 
    GSTVerificationReportSerializer, 
    UdyamReportSerializer, 
    ProfileAdvanceReportSerializer, 
    EquifaxV3ReportSerializer, 
    GSTTurnoverReportSerializer,
    MobileToAccountNumberSerializer,
    MobileToDLLookupSerializer,
    PanAllInOneSerializer,
    DigitalPaymentAnalyserSerializer
)

from .utils import (
    fetch_mobile360_data, 
    fetch_uan_employment_data, 
    fetch_uan_history_data, 
    fetch_esic_data, 
    fetch_gst_data, 
    fetch_gst_turnover_data, 
    fetch_udyam_data, 
    fetch_mobile_to_account_data, 
    fetch_profile_advance_data,
    fetch_equifax_data,
    fetch_mobile_to_dl_data,
    get_uan_dtls_without_otp,
    fetch_pan_all_in_one_data,
    fetch_digital_payment_analyser_data
)

@api_view(["POST"])
# @permission_classes([IsAuthenticated])
def mobile_360_search(request):
    mobile_number = request.data.get("mobile_number")
    realtime_data = request.data.get("realtimeData", False)

    if not mobile_number:
        return Response(create_response(False, "mobile_number is required", None), status=status.HTTP_400_BAD_REQUEST)

    if not realtime_data:
        try:
            report = Mobile360Report.objects.get(mobile_number=mobile_number)
            serialized = Mobile360ReportSerializer(report).data
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)

        except Mobile360Report.DoesNotExist:
            pass

    try:
        result_data = fetch_mobile360_data(mobile_number)

        # if result_data['success']:
        Mobile360Report.objects.update_or_create(
            mobile_number=mobile_number,
            defaults={"result": result_data['data']}
        )

        return Response(create_response(True, "Data fetched from external API", result_data['data']), status=status.HTTP_200_OK)
        
    except Exception as e:
            return Response(create_response(False, f"Unexpected error: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def uan_history_search(request):
    uan_no_list = request.data.get("uanNoList", [])
    realtime_data = request.data.get("realtimeData", False)

    if not uan_no_list or not isinstance(uan_no_list, list):
        return Response(create_response(False, "uanNoList must be a non-empty list", None), status=status.HTTP_400_BAD_REQUEST)
        # return Response({
        #     "status": False,
        #     "message": "uanNoList must be a non-empty list",
        #     "data": None
        # }, status=status.HTTP_400_BAD_REQUEST)

    results = []
    for uan_no in uan_no_list:
        if not realtime_data:
            try:
                report = UANHistoryReport.objects.get(uan=uan_no)
                results.append({
                    "uan": uan_no,
                    "source": "database",
                    "data": UANHistoryReportSerializer(report).data['result']
                })
                continue
            except UANHistoryReport.DoesNotExist:
                # results.append({
                #     "uan": uan_no,
                #     "source": "database",
                #     "error": "No data found in database"
                # })
                # continue
                pass

        # realtime_data = True or fallback to API
        api_response = fetch_uan_history_data(uan_no)
        print("API RESPONSE: ", api_response)
        if api_response.get("success"):
            data = api_response["data"]
            report, _ = UANHistoryReport.objects.update_or_create(
                uan=uan_no,
                defaults={
                    "result": data.get("result", {})
                }
            )
            results.append({
                "uan": uan_no,
                "source": "external_api",
                "data": api_response["data"]['result']
            })
        else:
            results.append({
                "uan": uan_no,
                "source": "external_api",
                "error": "External API did not respond or returned an error."
            })
    return Response(create_response(True, "External API did not respond or returned an error." if not api_response.get('success') else  "Data fetched from external API" if realtime_data else "Data fetched from database", results), status=status.HTTP_200_OK if api_response.get("success") else status.HTTP_404_NOT_FOUND)
    # return Response({
    #     "status": True,
    #     "message": "Data processed successfully",
    #     "data": {"results": results}
    # }, status=status.HTTP_200_OK)

@api_view(["POST"])
def uan_employment_search(request):
    uan_no_list = request.data.get("uanNoList", [])
    realtime_data = request.data.get("realtimeData", False)

    if not uan_no_list:
        return Response(create_response(False, "uanNoList is required", None), status=status.HTTP_400_BAD_REQUEST)
        # return Response({"error": "uanNoList is required"}, status=status.HTTP_400_BAD_REQUEST)

    results = []

    for uan in uan_no_list:
        if not realtime_data:
            try:
                report = UANEmploymentReport.objects.get(uan=uan)
                serialized = UANEmploymentReportSerializer(report).data
                results.append({"uan": uan, "source": "db", "data": serialized['result']})
                continue
            except UANEmploymentReport.DoesNotExist:
                # results.append({"uan": uan, "source": "db", "error": "No record found in DB"})
                # continue
                pass
        else:
            # Real-time or fallback if DB not found
            api_response = fetch_uan_employment_data(uan)

            if api_response.get("success"):
                data = api_response["data"]
                report, _ = UANEmploymentReport.objects.update_or_create(
                    uan=uan,
                    defaults={
                        "result": data.get("result", {})
                    }
                )
                serialized = UANEmploymentReportSerializer(report).data
                results.append({"uan": uan, "source": "api", "data": serialized['result']})
            else:
                results.append({
                    "uan": uan,
                    "source": "api",
                    "error": "API did not respond or returned an error."
                })

    return Response(create_response(True, "Data processed successfully", results), status=status.HTTP_200_OK)
    # return Response(results, status=status.HTTP_200_OK)

@api_view(['POST'])
def esic_search(request):
    esic_number = request.data.get("esic_number")
    realtime = request.data.get("realtimeData", False)

    if not esic_number:
        return Response(create_response(False, "Missing 'esic_number'", None), status=status.HTTP_400_BAD_REQUEST)

    if not realtime:
        try:
            report = ESICReport.objects.get(esic_number=esic_number)
            serialized = ESICReportSerializer(report).data
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)
        
        except ESICReport.DoesNotExist:
            pass
    
    try:
        fetch_result = fetch_esic_data(esic_number)

        # if fetch_result['success']:
        result_data = fetch_result["data"]
        ESICReport.objects.update_or_create(
            esic_number=esic_number,
            defaults={"result": result_data}
        )
        return Response(create_response(True, "Data fetched from external API", result_data), status=status.HTTP_200_OK)
        # return Response({
        #     "message": "Data fetched from external API",
        #     "data": result_data
        # }, status=status.HTTP_200_OK)
        
        # else:
        #     # If fetch fails or result not available
        #     return Response(create_response(False, fetch_result.get('error') if 'error' in fetch_result else "Internal Error", None), status=status.HTTP_404_NOT_FOUND)
            # return Response(
            #     {"error": "API did not respond or returned an error."},
            #     status=status.HTTP_502_BAD_GATEWAY
            # )
    # except requests.exceptions.RequestException as e:
    #     return Response(create_response(False, f"API request failed: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)
    # except json.JSONDecodeError:
    #     return Response(create_response(False, "Failed to parse API response", None), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(create_response(False,f"Unexpected error: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def gst_verification_search(request):
    gst_no = request.data.get("gst_no")
    realtime_data = request.data.get("realtimeData", False)

    if not gst_no:
        return Response(create_response(False, "gst_no is required", None), status=status.HTTP_400_BAD_REQUEST)

    if not realtime_data:
        try:
            report = GSTVerificationReport.objects.get(gst_no=gst_no)
            serialized = GSTVerificationReportSerializer(report).data
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)
        
        except GSTVerificationReport.DoesNotExist:
            pass
        
    try:
        api_response = fetch_gst_data(gst_no)

        # if api_response['success']:
        result_data = api_response["data"]

        GSTVerificationReport.objects.update_or_create(
            gst_no=gst_no,
            defaults={"result": result_data}
        )
        return Response(create_response(True, "Data fetched from external API", result_data), status=status.HTTP_200_OK)
        # else:
        #     return Response(create_response(False, api_response.get('error') if 'error' in api_response else "Internal Error", None), status=status.HTTP_404_NOT_FOUND)
    # except requests.exceptions.RequestException as e:
    #     return Response(create_response(False, f"API request failed: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)
    # except json.JSONDecodeError:
    #     return Response(create_response(False, "Failed to parse API response", None), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(create_response(False, str(e), None), status=status.HTTP_404_NOT_FOUND)
        # return Response({"error": str(e)}, status=status.HTTP_404_NOT_FOUND)
@api_view(["POST"])
def gst_turnover_search(request):
    gst_no = request.data.get("gst_no")
    year = request.data.get("year")
    realtime_data = request.data.get("realtimeData", False)

    if not gst_no or not year:
        return Response(create_response(False, "gst_no and year are required", None), status=status.HTTP_400_BAD_REQUEST)
        # return Response({"error": "gst_no and year are required"}, status=status.HTTP_400_BAD_REQUEST)

    if not realtime_data:
        try:
            report = GSTTurnoverReport.objects.get(gst_no=gst_no, year=year)
            serialized = GSTTurnoverReportSerializer(report).data
            # return Response(create_response(True, "Data fetched from database", report.result), status=status.HTTP_200_OK)
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)
            # return Response({
            #     "message": "Data fetched from database",
            #     "data": report.result
            # }, status=status.HTTP_200_OK)
        except GSTTurnoverReport.DoesNotExist:
            pass
            # return Response(create_response(False, "No data found in database for this GST number and year", None), status=status.HTTP_404_NOT_FOUND)
            # return Response({
            #     "message": "No data found in database for this GST number and year"
            # }, status=status.HTTP_404_NOT_FOUND)
    try:
        # realtime_data == True
        api_response = fetch_gst_turnover_data(gst_no, year)

        # if api_response.get("success") and "result" in api_response.get("data", {}):
        result_data = api_response["data"]

        GSTTurnoverReport.objects.update_or_create(
            gst_no=gst_no,
            year=year,
            defaults={"result": result_data}
        )
        return Response(create_response(True, "Data fetched from external API", result_data), status=status.HTTP_200_OK)
        # else:
        #     return Response(create_response(False, api_response.get('error') if 'error' in api_response else "Internal Error", None), status=status.HTTP_404_NOT_FOUND)
    # except requests.exceptions.RequestException as e:
    #     return Response(create_response(False, f"API request failed: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)
    # except json.JSONDecodeError:
    #     return Response(create_response(False, "Failed to parse API response", None), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(create_response(False, str(e), None), status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def udyam_verification_search(request):
    registration_no = request.data.get("registration_no")
    realtime_data = request.data.get("realtimeData", False)

    if not registration_no:
        return Response(create_response(False, "registration_no is required", None), status=status.HTTP_400_BAD_REQUEST)
        # return Response({"error": "registration_no is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not realtime_data:
        try:
            print("registraion_no: ", registration_no)
            report = UdyamReport.objects.get(registration_no=registration_no)
            serialized = UdyamReportSerializer(report).data
            # return Response(create_response(True, "Data fetched from database", report.result), status=status.HTTP_200_OK)
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)
            # return Response({
            #     "message": "Data fetched from database",
            #     "data": report.result  # ✅ return only the JSON-serializable result
            # }, status=status.HTTP_200_OK)
        except UdyamReport.DoesNotExist:
            pass
            # return Response(create_response(False, "No data found in database for this Udyam number", None), status=status.HTTP_404_NOT_FOUND)
            # return Response({
            #     "message": "No data found in database for this Udyam number"
            # }, status=status.HTTP_404_NOT_FOUND)
    try:
        # Fetch fresh data from external API
        api_response = fetch_udyam_data(registration_no)

        # if api_response.get("success") and "result" in api_response.get("data", {}):
        result_data = api_response["data"]
        UdyamReport.objects.update_or_create(
            registration_no=registration_no,
            defaults={"result": result_data}
        )
        return Response(create_response(True, "Data fetched from external API", result_data), status=status.HTTP_200_OK)
            # return Response({
            #     "message": "Data fetched from external API",
            #     "data": result_data
            # }, status=status.HTTP_200_OK)
    #     else:
    #         return Response(create_response(False, api_response.get('error') if 'error' in api_response else "Internal Error", None), status=status.HTTP_404_NOT_FOUND)
    # except requests.exceptions.RequestException as e:
    #     return Response(create_response(False, f"API request failed: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)
    # except json.JSONDecodeError:
    #     return Response(create_response(False, "Failed to parse API response", None), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(create_response(False, str(e), None), status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def profile_advance_search(request):
    mobile = request.data.get("mobile_number")
    realtime_data = request.data.get("realtimeData", False)

    if not mobile:
        return Response(create_response(False, "mobile is required", None), status=status.HTTP_400_BAD_REQUEST)
        # return Response({"error": "mobile is required"}, status=status.HTTP_400_BAD_REQUEST)

    if not realtime_data:
        try:
            report = ProfileAdvanceReport.objects.get(mobile=mobile)
            serialized = ProfileAdvanceReportSerializer(report).data
            # return Response(create_response(True, "Data fetched from database", report.result), status=status.HTTP_200_OK)
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)
            # return Response({
            #     "message": "Data fetched from database",
            #     "data": report.result
            # }, status=status.HTTP_200_OK)
        except ProfileAdvanceReport.DoesNotExist:
            pass
            # return Response(create_response(False, "No data found in database for this mobile number", None), status=status.HTTP_404_NOT_FOUND)
            # return Response({
            #     "message": "No data found in database for this mobile number"
            # }, status=status.HTTP_404_NOT_FOUND)

    try:
    # Fetch fresh data from external API
        api_response = fetch_profile_advance_data(mobile)

        # if api_response.get("success") and "result" in api_response.get("data", {}):
        result_data = api_response["data"]

        ProfileAdvanceReport.objects.update_or_create(
            mobile=mobile,
            defaults={"result": result_data}
        )
        return Response(create_response(True, "Data fetched from external API", result_data), status=status.HTTP_200_OK)
        # return Response({
            #     "message": "Data fetched from external API",
            #     "data": result_data
            # }, status=status.HTTP_200_OK)
    #     else:
    #         return Response(create_response(False, api_response.get('error') if 'error' in api_response else "Internal Error", None), status=status.HTTP_404_NOT_FOUND)
    # except requests.exceptions.RequestException as e:
    #     return Response(create_response(False, f"API request failed: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)
    # except json.JSONDecodeError:
    #     return Response(create_response(False, "Failed to parse API response", None), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(create_response(False, str(e), None), status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def equifax_v3_search(request):
    mobile = request.data.get("mobile")
    name = request.data.get("name")
    id_number = request.data.get("id_number")
    id_type = request.data.get("id_type")
    realtime_data = request.data.get("realtimeData", False)

    if not all([mobile, name, id_number, id_type]):
        return Response(create_response(False, "Missing one or more required fields: mobile, name, id_number, id_type", None), status=status.HTTP_400_BAD_REQUEST)
        # return Response({"error": "Missing one or more required fields: mobile, name, id_number, id_type"}, status=status.HTTP_400_BAD_REQUEST)

    if not realtime_data:
        try:
            report = EquifaxV3Report.objects.get(mobile=mobile)
            serialized = EquifaxV3ReportSerializer(report).data
            # return Response(create_response(True, "Data fetched from database", report.result), status=status.HTTP_200_OK)
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)
            # return Response({
            #     "message": "Data fetched from database",
            #     "data": report.result
            # }, status=status.HTTP_200_OK)
        except EquifaxV3Report.DoesNotExist:
            pass
            # return Response(create_response(False, "No data found in database for this mobile number", None), status=status.HTTP_404_NOT_FOUND)
            # return Response({
            #     "message": "No data found in database for this mobile number"
            # }, status=status.HTTP_404_NOT_FOUND)

    try:
        # Fetch from external API
        api_response = fetch_equifax_data(id_number, id_type, mobile, name)

        # if api_response.get("success") and "result" in api_response.get("data", {}):
        result_data = api_response["data"]

        EquifaxV3Report.objects.update_or_create(
            mobile=mobile,
            defaults={
                "name": name,
                "id_number": id_number,
                "id_type": id_type,
                "result": result_data
            }
        )
        return Response(create_response(True, "Data fetched from external API", result_data), status=status.HTTP_200_OK)
            # return Response({
            #     "message": "Data fetched from external API",
            #     "data": result_data
            # }, status=status.HTTP_200_OK)
    #     else:
    #         return Response(create_response(False, api_response.get('error') if 'error' in api_response else "Internal Error", None), status=status.HTTP_404_NOT_FOUND)
    # except requests.exceptions.RequestException as e:
    #     return Response(create_response(False, f"API request failed: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)
    # except json.JSONDecodeError:
    #     return Response(create_response(False, "Failed to parse API response", None), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(create_response(False, str(e), None), status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
def get_acc_dtls_from_mobile(request):
    mobile_number = request.data.get("mobile_number")
    realtime_data = request.data.get("realtimeData", False)

    if not mobile_number:
        return Response(create_response(False, "mobile_number is required", None), status=status.HTTP_400_BAD_REQUEST)

    if not realtime_data:
        try:
            report = MobileToAccountNumber.objects.get(mobile_number=mobile_number)
            serialized = MobileToAccountNumberSerializer(report).data
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)
        except MobileToAccountNumber.DoesNotExist:
            pass
            # return Response(create_response(False, "No data found in database for this mobile number", None), status=status.HTTP_404_NOT_FOUND)

    try:
        # Fetch fresh data from external API
        api_response = fetch_mobile_to_account_data(mobile_number)

        # if api_response.get("success") and "data" in api_response:
        result_data = api_response["data"]

        MobileToAccountNumber.objects.update_or_create(
            mobile_number=mobile_number,
            defaults={"result": result_data}
        )
        return Response(create_response(True, "Data fetched from external API", result_data), status=status.HTTP_200_OK)
    #     else:
    #         return Response(create_response(False, api_response.get('error') if 'error' in api_response else "Internal Error", None), status=status.HTTP_404_NOT_FOUND)
    # except requests.exceptions.RequestException as e:
    #     return Response(create_response(False, f"API request failed: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)
    # except json.JSONDecodeError:
        return Response(create_response(False, "Failed to parse API response", None), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(create_response(False, str(e), None), status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
def uan_passbook_without_otp(request):
    uan_no_list = request.data.get("uanNoList", [])
    realtime_data = request.data.get("realtimeData", False)

    if not uan_no_list:
        return Response(create_response(False, "uanNoList is required", None), status=status.HTTP_400_BAD_REQUEST)

    results = []

    for uan in uan_no_list:
        if not realtime_data:
            try:
                report = UanWithoutOtp.objects.get(uan=uan)
                serialized = UanWithoutOtpSerializer(report).data
                results.append({"uan": uan, "source": "db", "data": serialized['result']})
                continue
            except UanWithoutOtp.DoesNotExist:
                pass
                # results.append({"uan": uan, "source": "db", "error": "No record found in DB"})
                # continue

        # Real-time or fallback if DB not found
        api_response = get_uan_dtls_without_otp(uan)

        if api_response.get("success"):
            data = api_response["data"]
            report, _ = UanWithoutOtp.objects.update_or_create(
                uan=uan,
                defaults={
                    "result": data
                }
            )
            serialized = UanWithoutOtpSerializer(report).data
            results.append({"uan": uan, "source": "api", "data": serialized['result']})
        else:
            results.append({
                "uan": uan,
                "source": "api",
                "error": "API did not respond or returned an error."
            })

    return Response(create_response(True, "Data processed successfully", results), status=status.HTTP_200_OK)


@api_view(["POST"])
def mobile_to_dl_lookup(request):
    mobile_number = request.data.get("mobile_number")
    name = request.data.get("name")
    dob = request.data.get("dob")
    realtime_data = request.data.get("realtimeData", False)

    if not mobile_number or not name or not dob:
        return Response(create_response(False, "mobile_number and name and dob are required", None), status=status.HTTP_400_BAD_REQUEST)

    if not realtime_data:
        try:
            report = MobileToDLLookup.objects.get(mobile_number=mobile_number)
            serialized = MobileToDLLookupSerializer(report).data
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)
        except MobileToDLLookup.DoesNotExist:
            pass
            # return Response(create_response(False, "No data found in database for this mobile number", None), status=status.HTTP_404_NOT_FOUND)

    try:
        # Fetch fresh data from external API
        api_response = fetch_mobile_to_dl_data(mobile_number, name, dob)

        # if api_response.get("success") and "data" in api_response:
        result_data = api_response["data"]

        MobileToDLLookup.objects.update_or_create(
            mobile_number=mobile_number,
            defaults={"result": result_data}
        )
        return Response(create_response(True, "Data fetched from external API", result_data), status=status.HTTP_200_OK)
    #     else:
    #         return Response(create_response(False, api_response.get('error') if 'error' in api_response else "Internal Error", None), status=status.HTTP_404_NOT_FOUND)
    # except requests.exceptions.RequestException as e:
    #     return Response(create_response(False, f"API request failed: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)
    # except json.JSONDecodeError:
        return Response(create_response(False, "Failed to parse API response", None), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(create_response(False, str(e), None), status=status.HTTP_404_NOT_FOUND)
    
@api_view(["POST"])
def pan_all_in_one(request):
    print("Called")
    pan_number = request.data.get("pan_number")
    realtime_data = request.data.get("realtimeData", False)

    if not pan_number:
        return Response(create_response(False, "pan_number is required", None), status=status.HTTP_400_BAD_REQUEST)

    if not realtime_data:
        try:
            pan_report = PanAllInOne.objects.get(pan_number=pan_number)
            serialized = PanAllInOneSerializer(pan_report).data
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)
        
        except PanAllInOne.DoesNotExist:
            pass
            # return Response(create_response(False, "No data found in database for this PAN number", None), status=status.HTTP_404_NOT_FOUND)
        
    try:
        api_response = fetch_pan_all_in_one_data(pan_number)
        
        # if api_response.get("success") and "data" in api_response:
        result_data = api_response["data"]

        PanAllInOne.objects.update_or_create(
            pan_number=pan_number,
            defaults={"result": result_data}
        )

        return Response(create_response(True, "Data fetched from external API", result_data), status=status.HTTP_200_OK)
    
    #     else:
    #         return Response(create_response(False, api_response.get('error') if 'error' in api_response else "Internal Error", None), status=status.HTTP_404_NOT_FOUND)
    # except requests.exceptions.RequestException as e:
    #     return Response(create_response(False, f"API request failed: {str(e)}", None), status=status.HTTP_404_NOT_FOUND)
    # except json.JSONDecodeError:
    #     return Response(create_response(False, "Failed to parse API response", None), status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response(create_response(False, str(e), None), status=status.HTTP_404_NOT_FOUND)
    
@api_view(["POST"])
def digital_payment_analyser(request):
    mobile_number = request.data.get("mobile_number")
    realtime_data = request.data.get("realtimeData", False)

    if not mobile_number:
        return Response(create_response(False, "mobile_number is required", None), status=status.HTTP_400_BAD_REQUEST)

    if not realtime_data:
        try:
            report = DigitalPaymentAnalyser.objects.get(mobile_number=mobile_number)
            serialized = DigitalPaymentAnalyserSerializer(report).data
            return Response(create_response(True, "Data fetched from database", serialized['result']), status=status.HTTP_200_OK)

        except DigitalPaymentAnalyser.DoesNotExist:
            pass
            # return Response(create_response(False, "No data found in the database for this mobile number."))
    
    try:
        api_response = fetch_digital_payment_analyser_data(mobile_number=mobile_number)
        if api_response:
            DigitalPaymentAnalyser.objects.update_or_create(
                mobile_number=mobile_number,
                defaults={"result": api_response}
            )
            return Response(create_response(True, "Data fetched from external API", api_response), status=status.HTTP_200_OK)
        
        else:
            return Response(create_response(False, "No digital payments found.", data=None), status=status.HTTP_200_OK)
    except Exception as e:

        return Response(create_response(False, str(e), None), status=status.HTTP_404_NOT_FOUND)
