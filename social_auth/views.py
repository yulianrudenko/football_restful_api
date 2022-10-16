from core.custom import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import FacebookSocialAuthSerializer, GoogleSocialAuthSerializer


class FacebookSocialAuthView(APIView):
    permission_classes = [AllowAny]
    serializer_class = FacebookSocialAuthSerializer

    def post(self, request, *args, **kwargs):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_credentials = serializer.validated_data['auth_token']
        return Response(user_credentials, status=status.HTTP_200_OK)


class GoogleSocialAuthView(APIView):
    permission_classes = [AllowAny]
    serializer_class = GoogleSocialAuthSerializer

    def post(self, request, *args, **kwargs):
        """
        POST with "auth_code"
        Send an authentication code from google to get id_token and thus user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_credentials = serializer.validated_data['auth_code']
        return Response(user_credentials, status=status.HTTP_200_OK)
