import jwt

from core.custom import APIView, CustomJSONRenderer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    PasswordResetSerializer
)
from .services import verify_token
from .utlis import login_user


class RegisterView(APIView):
    permission_classes = [AllowAny]
    renderer_classes = [CustomJSONRenderer]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = login_user(**serializer.validated_data)
        response = {
            'email': user.email,
            'username': user.username,
            'tokens': user.get_tokens()
        }
        return Response(response, status=status.HTTP_200_OK)


class RequestPasswordResetView(APIView):
    serializer_class = PasswordResetSerializer

    def post(self, reqeust):
        serializer = self.serializer_class(data=reqeust.data)
        serializer.is_valid(raise_exception=True)
