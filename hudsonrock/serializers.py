from rest_framework import serializers
from .models import HudsonRockData

class HudsonRockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HudsonRockData
        fields = '__all__'

    def validate_data_type(self, value):
        valid_types = ['email', 'domain']  # Add other valid types
        if value not in valid_types:
            raise serializers.ValidationError(f"Invalid data type. Must be one of {valid_types}")
        return value