from rest_framework import serializers

class DynamoDBItemSerializer(serializers.Serializer):
    class Meta:
        extra_kwargs = {'mobno': {'required': True}}

    def to_representation(self, instance):
        data = super().to_representation(instance)
        for key, value in instance.items():
            if isinstance(value, type('')):
                data[key] = value
            elif isinstance(value, (int, float)):
                data[key] = value
            elif isinstance(value, list):
                data[key] = value
            elif isinstance(value, dict):
                data[key] = value
            elif isinstance(value, Decimal):
                if value % 1 == 0:
                    data[key] = int(value)
                else:
                    data[key] = float(value)
            else:
                data[key] = str(value)
        return data