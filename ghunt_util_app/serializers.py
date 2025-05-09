from rest_framework import serializers
from .models import TokenUpdationLog

class TokenSerializer(serializers.Serializer):
    token = serializers.JSONField(required=True)

class TokenUpdationLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = TokenUpdationLog
        fields = '__all__'