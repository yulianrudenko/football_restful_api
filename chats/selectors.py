from rest_framework.exceptions import NotFound

from .models import Chat


def get_chat(id: int) -> Chat:
    try:
        chat = Chat.objects.get(id=id)
    except:
        raise NotFound(detail='Chat with given id does not exist.')
    return chat
