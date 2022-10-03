from rest_framework import serializers
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator

from .models import User


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
        '''username validation only'''
        username = attrs.get('username')
        if not username.isalnum():
            raise ValidationError('Only letters and numbers are allowed for username.')
        return attrs
