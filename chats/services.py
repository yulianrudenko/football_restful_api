from django.db import transaction
from django.db import connection
from rest_framework.validators import ValidationError

from authentication.models import User
from .models import Chat


@transaction.atomic
def start_chat(*, user1: User, user2: User) -> int:
    '''Check if chat already exists, if not -> create'''
    if user1 == user2:
        raise ValidationError(detail='Impossible to create chat with 1 user')

    with connection.cursor() as cursor:
        query = f'''
            SELECT chat_id
            FROM chats_chat_users
            WHERE user_id IN ({user1.id}, {user2.id})
            GROUP BY chat_id
            HAVING Count(chat_id) > 1;'''
        cursor.execute(query)
        queryset = cursor.fetchone()

    if queryset:
        chat_id = queryset[0]
        return chat_id

    chat = Chat.objects.create()
    chat.save()
    chat.users.add(user1, user2)
    return chat.id
