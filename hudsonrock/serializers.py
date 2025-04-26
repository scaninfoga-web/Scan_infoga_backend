from rest_framework import serializers
from .models import HudsonRockData

class HudsonRockDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = HudsonRockData
        fields = '__all__'