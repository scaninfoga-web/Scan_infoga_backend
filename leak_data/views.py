# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated

# from core.utils import create_response
# from .utils import LeakEmailPasswords

# @api_view(['GET'])
# # @permission_classes([IsAuthenticated])
# def get_passwords(request):
#     email = request.data.get('email')
#     if not email:
#         return Response(create_response(False, "Email is required", None), status=status.HTTP_400_BAD_REQUEST)
#     leak_email_passwords = LeakEmailPasswords()
#     passwords = leak_email_passwords.fetch_passwords(email)
#     return Response(create_response(True, "Data fetched from Database.", passwords), status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from botocore.exceptions import ClientError
from django.conf import settings

from .utils import get_leaked_credentials_dynamodb_table,get_jobseeker_dynamodb_table
from .serializers import DynamoDBItemSerializer
from core.utils import create_response

class GetPassword(APIView):
    def post(self, request, format=None):
        email = request.data.get('email')

        if not email:
            return Response(create_response(True, "Email is required in the request body.", None),status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(email, str):
            return Response(create_response(True, "Email must be a string.", None),status=status.HTTP_400_BAD_REQUEST)

        try:
            users_table = get_leaked_credentials_dynamodb_table()
            response = users_table.get_item(
                Key={'email': email}
            )
            item = response.get('Item')

            if item:
                serializer = DynamoDBItemSerializer(item)
                response = serializer.data
                return Response(create_response(True, "Data fetched from Database.", response), status=status.HTTP_200_OK)
            else:
                return Response(create_response(False, "Email not found in database.", None),status=status.HTTP_404_NOT_FOUND)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                return Response(create_response(False, "DynamoDB table not found. Check DYNAMODB_TABLE_NAME setting.", None),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            print(f"DynamoDB ClientError: {e}")
            return Response(create_response(False, "A DynamoDB error occurred while searching.", None),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response(create_response(False, "An unexpected error occurred.", None),status=status.HTTP_500_INTERNAL_SERVER_ERROR)




class GetJobSeekerData(APIView):
    def post(self, request, format=None):
        mobno = request.data.get('mobile')
        if not mobno:
            return Response(create_response(True, "Mobile number is required in the request body.", None),status=status.HTTP_400_BAD_REQUEST)
        if not isinstance(mobno, str):
            return Response(create_response(True, "Mobile number must be a string.", None),status=status.HTTP_400_BAD_REQUEST)

        if len(mobno) != 10:
            return Response({"error": "Mobile number must be 10 digits."},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            users_table = get_jobseeker_dynamodb_table()
            response = users_table.get_item(
                Key={'mobile_number': mobno}
            )
            item = response.get('Item')

            if item:
                serializer = DynamoDBItemSerializer(item)
                response = serializer.data
                return Response(create_response(True, "Data fetched from Database.", response), status=status.HTTP_200_OK)
            else:
                return Response(create_response(False, "Mobile number not found in database.", None),status=status.HTTP_404_NOT_FOUND)
        except ClientError as e:
            if e.response['Error']['Code'] == 'ResourceNotFoundException':
                return Response(create_response(False, "DynamoDB table not found. Check DYNAMODB_TABLE_NAME setting.", None),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            print(f"DynamoDB ClientError: {e}")
            return Response(create_response(False, "A DynamoDB error occurred while searching.", None),status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(f"Unexpected error: {e}")
            return Response(create_response(False, "An unexpected error occurred.", None),status=status.HTTP_500_INTERNAL_SERVER_ERROR)