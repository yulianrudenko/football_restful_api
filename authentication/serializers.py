from django.conf import settings
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import AuthenticationFailed

from core.validators import username_validator

from .models import User


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(User.objects.all(), message='User with provided email already exists.')])
    username = serializers.CharField(
        validators=[
            UniqueValidator(User.objects.all(), message='This username is already taken.'), 
            username_validator])

