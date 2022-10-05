import jwt

from core.views import APIView
from rest_framework.serializers import ValidationError
from rest_framework.validators import UniqueValidator
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .models import User
# from .serializers import RegisterSerializer
from .services import create_user, verify_token, login_user


class RegisterView(APIView):
    class RegisterInputSerializer(serializers.Serializer):
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

    input_serializer_class = RegisterInputSerializer

    def post(self, request):
        serializer = self.input_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        create_user(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    token_parameters = openapi.Parameter(name='token', in_=openapi.IN_QUERY,
        description='token', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_parameters])
    def get(self, request):
        token = request.GET.get('token')
        try:
            verify_token(token=token)           
            return Response({'email': 'Successfully verified'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError:
            return Response({'error': 'Activation link expired'}, status=status.HTTP_400_BAD_REQUEST) 
        except jwt.exceptions.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST) 


class LoginView(APIView):
    class LoginInputSerializer(serializers.Serializer):
        email = serializers.EmailField(min_length=4, max_length=250)
        password = serializers.CharField(min_length=4, max_length=250, write_only=True)

    input_serializer_class = LoginInputSerializer
    permission_classes = []

    def post(self, request):
        print(request.data)
        serializer = self.input_serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = login_user(**serializer.validated_data)
        response = {
            'email': user.email,
            'username': user.username,
            'tokens': user.get_tokens()
        }
        return Response(response, status=status.HTTP_200_OK)
