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
    RequestPasswordResetSerializer,
    PerformPasswordResetSerializer
)
from .services import user_create, user_activate_by_token

from .selectors import get_user
from .utlis import login_user, send_password_reset_email, validate_password_reset_token


class RegisterView(APIView):
    '''Register'''
    permission_classes = [AllowAny]
    renderer_classes = [CustomJSONRenderer]
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_create(**serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    '''Verify email'''
    token_parameters = openapi.Parameter(name='token', in_=openapi.IN_QUERY,
        description='token', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_parameters])
    def get(self, request):
        token = str(request.GET.get('token'))
        user_activate_by_token(token=token)           
        return Response({'email': 'Successfully verified'}, status=status.HTTP_200_OK)


class LoginView(APIView):
    '''Log in'''
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = login_user(**serializer.validated_data)
        response = {
            'email': user.email,
            'username': user.username,
            'tokens': user.get_tokens()}
        return Response(response, status=status.HTTP_200_OK)


class RequestPasswordResetView(APIView):
    '''Send link for password reset to provided user's email'''
    permission_classes = [AllowAny]
    serializer_class = RequestPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        send_password_reset_email(to_email=email)
        return Response({'success': f'Email with link to reset password was sent to {email}'},
            status=status.HTTP_200_OK)


class TokenCheckPasswordResetView(APIView):
    '''Decode userId and check token, then return them back'''
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        if validate_password_reset_token(uidb64=uidb64, token=token):
            return Response({'uidb64': uidb64, 'token': token}, status=status.HTTP_200_OK)


class PerformPasswordResetSerializer(APIView):
    '''Perform password update with the one entered by user'''
    permission_classes = [AllowAny]
    serializer_class = PerformPasswordResetSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_password = serializer.validated_data.get('new_password')
        uidb64 = serializer.validated_data.get('uidb64')
        token = serializer.validated_data.get('token')
        user = validate_password_reset_token(uidb64=uidb64, token=token)
        user.set_password(new_password)
        user.save()
        return Response({'success': f'Updated password for {user.username}'}, status=status.HTTP_200_OK)
