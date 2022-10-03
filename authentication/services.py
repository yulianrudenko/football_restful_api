import jwt

from django.conf import settings
from django.contrib import auth
from django.db import transaction
from rest_framework.exceptions import AuthenticationFailed

from .models import User
from .utlis import send_activation_email


@transaction.atomic
def create_user(*, email: str, username: str, password: str) -> User:
    new_user = User.objects.create_user(
        email=email,
        username=username,
        password=password,
        is_verified=True)
    # send_activation_email(to_user=new_user)
    return new_user


def verify_token(*, token: str) -> None:
    '''verify token in order to verify newly registered user'''
    payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms='HS256')  # payload == данные или сообщения, передаваемые по сети 
    user = User.objects.get(id=payload['user_id'])
    if not user.is_verified:
        user.is_verified = True
        user.save()


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
