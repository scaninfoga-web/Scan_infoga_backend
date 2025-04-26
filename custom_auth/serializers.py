from rest_framework import serializers
from .models import CustomUser, DeveloperProfile, CorporateProfile
import hashlib

class UserRegistrationSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'firstName', 'lastName']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        email = validated_data.pop('email')
        
        user = CustomUser.objects.create_user(
            email=email,
            password=hashed_password,
            user_type='USER',
            **validated_data
        )
        return user

class DeveloperRegistrationSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True)
    
    class Meta:
        model = DeveloperProfile
        fields = ['firstName', 'lastName', 'email', 'password']
        extra_kwargs = {'email': {'write_only': True}}

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user = CustomUser.objects.create_user(
            email=email,
            password=hashed_password,
            user_type='DEVELOPER'
        )
        
        developer = DeveloperProfile.objects.create(
            user=user,
            **validated_data
        )
        return developer

class CorporateRegistrationSerializer(serializers.ModelSerializer):
    firstName = serializers.CharField(source='first_name')
    lastName = serializers.CharField(source='last_name')
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True)  # Add this line
    userType = serializers.CharField(write_only=True, default='crp')  # Add this line
    
    class Meta:
        model = CorporateProfile
        fields = ['firstName', 'lastName', 'company', 'domain', 'email', 'password', 'userType']

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        validated_data.pop('userType', None)  # Remove userType from validated_data
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        user = CustomUser.objects.create_user(
            email=email,
            password=hashed_password,
            user_type='CORPORATE'
        )
        
        corporate = CorporateProfile.objects.create(
            user=user,
            **validated_data
        )
        return corporate