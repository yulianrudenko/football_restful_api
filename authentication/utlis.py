from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed
from django.contrib import auth
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.timezone import timedelta
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import smart_str, smart_bytes, force_str, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User


def send_activation_email(*, to_user: User) -> None:
    '''Send an activation link to new user's email'''
    
    # prepare body with activation link(containing acccess token)
    protocol = 'http' if settings.DEBUG else 'https'
    domain = settings.SITE_DOMAIN
    email_verify_path = reverse('auth:email_verify')
    access_token = RefreshToken.for_user(to_user).access_token
    access_token.set_exp(lifetime=timedelta(hours=12))
    link = f'{protocol}://{domain}{email_verify_path}?token={str(access_token)}'

    subject='Verify your email'
    body = f'Hi, {to_user.username}! Use link below to verify your email.\n{link}'
    email = EmailMessage(subject, body, from_email=settings.EMAIL_FROM_USER, to=[to_user])
    email.send()


def login_user(*, email: str, password: str) -> User:
    '''authenticate user if success return user instance'''
    user = auth.authenticate(email=email, password=password)
    if not user:
        raise AuthenticationFailed(detail='Invalid credentials')
    if not user.is_verified:
        raise AuthenticationFailed(detail='Email is not verified')
    if not user.is_active:
        raise AuthenticationFailed(detail='Account is not active, contact admin')
    return user


def send_password_reset_email(*, to_email: str) -> None:
    pass
