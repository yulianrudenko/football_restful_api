from django.conf import settings
from django.contrib import auth
from django.core.mail import EmailMessage
from django.urls import reverse
from django.utils.timezone import timedelta
from django.utils.encoding import smart_str, smart_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from rest_framework.exceptions import AuthenticationFailed, ValidationError, ParseError
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User
from .selectors import get_user


PROTOCOL = 'http' if settings.DEBUG else 'https'
DOMAIN = settings.SITE_DOMAIN


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


def send_activation_email(*, to_user: User) -> None:
    '''Send an activation link to new user's email. Generally used by services.user_create()'''
    
    # prepare body with activation link(containing acccess token)
    email_verify_path = reverse('auth:email-verify')
    access_token = RefreshToken.for_user(to_user).access_token
    access_token.set_exp(lifetime=timedelta(hours=12))
    link = f'{PROTOCOL}://{DOMAIN}{email_verify_path}?token={str(access_token)}'

    subject='Verify your email'
    body = f'Hi, {to_user.username}! Use link below to verify your email.\n{link}'
    email = EmailMessage(subject, body, from_email=settings.EMAIL_FROM_USER, to=[to_user])
    email.send()


def send_password_reset_email(*, to_email: str) -> None:
    '''Send an password reset link to user's email'''
    to_user = get_user(email=to_email)
    
    # prepare body with activation link(containing acccess token)
    uid64 = urlsafe_base64_encode(smart_bytes(to_user.id))
    token = PasswordResetTokenGenerator().make_token(user=to_user)
    password_reset_path = reverse('auth:confirm-password-reset',
        kwargs={'uidb64': uid64, 'token': token})
    link = f'{PROTOCOL}://{DOMAIN}{password_reset_path}'

    subject='Reset your password'
    body = f'Hi, {to_user.username}! Use link below to reset your password.\n{link}'
    email = EmailMessage(subject, body, from_email=settings.EMAIL_FROM_USER, to=[to_user])
    email.send()


def validate_password_reset_token(uidb64: str, token: str) -> User:
    try:
        user_id = smart_str(urlsafe_base64_decode(uidb64))
    except DjangoUnicodeDecodeError:
        raise ParseError(detail={'id': 'Failed to decode user id'})
    user = get_user(id=user_id)
    if not PasswordResetTokenGenerator().check_token(user=user, token=token):
        raise ValidationError(detail={'token': 'Invalid token'})
    return user
