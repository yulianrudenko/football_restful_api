import jwt

from django.conf import settings
from django.db import transaction
from rest_framework.exceptions import ValidationError

from .models import User
from .selectors import get_user
from .utlis import send_activation_email


@transaction.atomic
def user_create(*, email: str, username: str, password: str) -> User:
    new_user = User.objects.create_user(
        email=email,
        username=username,
        password=password,
        is_verified=False)
    send_activation_email(to_user=new_user)
    return new_user


@transaction.atomic
def user_activate_by_token(*, token: str) -> bool:
    '''validate token in order to "verify" newly registered user'''
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms='HS256')  # payload=данные или сообщения, передаваемые по сети 
    except jwt.ExpiredSignatureError:
        raise ValidationError({'error': 'Activation link expired'}) 
    except jwt.exceptions.DecodeError:
        raise ValidationError({'error': 'Invalid token'}) 
    except:
        raise ValidationError(detail='Invalid token')
    user = get_user(id=payload['user_id'])
    if not user.is_verified:
        user.is_verified = True
        user.save()
