from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HudsonRockData
from .serializers import HudsonRockDataSerializer
from core.utils import create_response

@api_view(['POST'])
def save_hudson_data(request):
    try:
        data = request.data
        data_type = data.pop('type', None)
        
        if not data or not data_type:
            return Response(
                create_response(
                    status=False,
                    message="Data and type are required",
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Add the type field to the data
        data['data_type'] = data_type
        
        serializer = HudsonRockDataSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                create_response(
                    status=True,
                    message="Data saved successfully",
                    data=serializer.data
                ),
                status=status.HTTP_201_CREATED
            )
        return Response(
            create_response(
                status=False,
                message="Invalid data",
                data=serializer.errors
            ),
            status=status.HTTP_400_BAD_REQUEST
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

@api_view(['GET'])
def get_hudson_data(request):
    try:
        data_type = request.GET.get('type')
        value = request.GET.get('value')
        
        if not data_type:
            return Response(
                create_response(
                    status=False,
                    message="Type parameter is required",
                    data=None
                ),
                status=status.HTTP_400_BAD_REQUEST
            )

        # Query based on data_type
        data = HudsonRockData.objects.filter(data_type=data_type)
        
        # If value is provided, filter by it
        if value:
            if data_type == 'email':
                # First get all records
                all_data = data.all()
                # Then filter in Python
                filtered_data = [
                    record for record in all_data
                    if any(
                        value.lower() in str(cred.get('username', '')).lower() 
                        for cred in record.credentials
                    )
                ]
                data = filtered_data
        
        # Use serializer appropriately based on whether data is filtered
        if isinstance(data, list):
            serializer = HudsonRockDataSerializer(data, many=True)
        else:
            serializer = HudsonRockDataSerializer(data.all(), many=True)
            
        return Response(
            create_response(
                status=True,
                message="Data retrieved successfully",
                data=serializer.data
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
