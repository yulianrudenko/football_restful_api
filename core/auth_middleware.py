import jwt

from django.contrib.auth.models import AnonymousUser
from django.conf import settings
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware

from authentication.models import User


@database_sync_to_async
def get_user(token_key) -> User | AnonymousUser:
    try:
        user_id: int = jwt.decode(token_key, settings.SECRET_KEY, algorithms='HS256').get('user_id')
    except jwt.exceptions.DecodeError:
        return None
    except jwt.exceptions.ExpiredSignatureError:
        return None
    try:
        return None if user_id is None else User.objects.get(id=user_id)
    except User.DoesNotExist:
        return None


class TokenAuthMiddleware(BaseMiddleware):
    '''
    Wrap WebSocket-request(scope) with additional value of User instance via token passed in query params
    Required for authentication inside consumers.py while connecting/sending messages
    '''
    def __init__(self, app):
        super().__init__(app)

    async def __call__(self, scope, receive, send):
        try:
            token_key = (dict((x.split('=') for x in scope['query_string'].decode().split("&")))).get('token', None)
        except ValueError:
            token_key = None
        scope['user'] = await get_user(token_key)
        return await super().__call__(scope, receive, send)