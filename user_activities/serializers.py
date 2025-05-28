from rest_framework import serializers
from .models import UserActivity

class UserActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserActivity
        fields = ['id', 'email', 'api_called', 'activity_time', 'request_payload', 'browser', 'ip_address', 'latitude', 'longitude']
        read_only_fields = ['id', 'activity_time']