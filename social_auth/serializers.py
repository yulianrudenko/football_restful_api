import os
import requests
from rest_framework import serializers

from . import facebook, google
from .services import register_social_user

GOOGLE_ID_TOKEN_INFO_URL = 'https://www.googleapis.com/oauth2/v3/tokeninfo'


class FacebookSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of Facebook related data"""
    auth_token = serializers.CharField()

    def validate_auth_token(self, auth_token):
        user_data = facebook.Facebook.validate(auth_token)
        try:
            email = user_data['email']
            name = user_data['name']
            return register_social_user(
                provider='Facebook',
                email=email,
                name=name)
        except Exception:
            raise serializers.ValidationError(
                'The token  is invalid or expired. Please try again.')


class GoogleSocialAuthSerializer(serializers.Serializer):
    """Handles serialization of Google related data"""
    auth_code = serializers.CharField()

    def validate_auth_code(self, auth_code):
        user_data = google.Google.validate(auth_code)
        try:
            email = user_data['email']
            name = email.split('@')[0]
        except Exception:
            raise serializers.ValidationError(
                'The token  is invalid or expired. Please try again.')
        return register_social_user(
            provider='Google',
            email=email,
            name=name)