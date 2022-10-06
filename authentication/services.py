import jwt
from django.conf import settings
from django.db import transaction

from .models import User
from .selectors import get_user
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


@transaction.atomic
def activate_user_by_token(*, token: str) -> bool:
    '''verify token in order to "activate" newly registered user'''
    payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms='HS256')  # payload == данные или сообщения, передаваемые по сети 
    user = get_user(id=payload['user_id'])
    if not user.is_verified:
        user.is_verified = True
        user.save()
