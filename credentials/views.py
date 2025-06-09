from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Credential

class GetPasswordView(APIView):
    def get(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            credential = Credential.objects.get(email=email)
            return Response({'email': credential.email, 'password': credential.password})
        except Credential.DoesNotExist:
            return Response({'error': 'Email not found'}, status=status.HTTP_404_NOT_FOUND)
