from django.db import transaction
from rest_framework.validators import ValidationError

from authentication.models import User
from .models import Chat


@transaction.atomic
def start_chat(*, user1: User, user2: User) -> int:
    print(user1, user2)
    if user1 == user2:
        raise ValidationError(detail='Impossible to create chat with 1 user')

    try:
        chat = Chat.objects.get(users__in=[user1, user2])
    except:
        chat = Chat.objects.create()
        chat.save()
        chat.users.add(user1, user2)
    return chat.id
