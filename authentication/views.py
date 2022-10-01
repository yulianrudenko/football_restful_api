from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse

from authentication.models import User

from .serializers import RegisterSerializer
from .services import send_activation_email


class RegisterView(APIView):
    def post(self, request):
        # validate data and create new user instance
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        new_user_data = serializer.data
        new_user = User.objects.create(**new_user_data)

        # prepare body with activation link(containing acccess token) for an activation email
        access_token = RefreshToken.for_user(new_user).access_token
        domain = get_current_site(request).domain
        email_verify_path = reverse('auth:email_verify')
        link = f'{request.scheme}://{domain}{email_verify_path}?token={str(access_token)}'
        email_body = f'Hi, {new_user.username}! Use link below to verify your email.\n{link}'

        send_activation_email(subject='Verify your email', body=email_body, to=new_user.email)

        return Response(new_user_data, status=status.HTTP_201_CREATED)


class VerifyEmailView(APIView):
    def get(self, request):
        pass
    