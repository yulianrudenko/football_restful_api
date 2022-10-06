from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import User
from .services import create_user


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(User.objects.all(), message='User with provided email already exists.')])
    username = serializers.CharField(
        min_length=4, 
        max_length=25,
        validators=[UniqueValidator(User.objects.all(), message='This username is already taken.')])
    password = serializers.CharField(
        min_length=5,
        max_length=50,
        write_only=True)

    def validate(self, attrs):
        '''validate username'''
        username = attrs.get('username')
        if not username.isalnum():
            raise serializers.ValidationError('Only letters and numbers are allowed for username.')
        return super().validate(attrs) 
    
    def create(self, validated_data):
        return create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=4, max_length=250)
    password = serializers.CharField(min_length=4, max_length=250, write_only=True)


class RequestPasswordResetSerializer(serializers.Serializer):
    '''serializer for email to send password reset URL'''
    email = serializers.EmailField(min_length=4)


class PerformPasswordResetSerializer(serializers.Serializer):
    '''serializer for new password given by user, encoded user_id and token itself'''
    password = serializers.CharField(min_length=5, write_only=True)
    uidb64 = serializers.CharField(min_length=1, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True)
