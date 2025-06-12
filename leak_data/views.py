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

