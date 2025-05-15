from rest_framework import serializers

class GHuntLoginSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)

class GHuntEmailInfoSerializer(serializers.Serializer):
    email = serializers.CharField(required=True)
    json_file = serializers.CharField(required=False, allow_null=True)