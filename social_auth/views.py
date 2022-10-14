from core.custom import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from .serializers import FacebookSocialAuthSerializer


class FacebookSocialAuthView(APIView):
    permission_classes = [AllowAny]
    serializer_class = FacebookSocialAuthSerializer

    def post(self, request):
        """
        POST with "auth_token"
        Send an access token as from facebook to get user information
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data['auth_token']
        return Response(data, status=status.HTTP_200_OK)
