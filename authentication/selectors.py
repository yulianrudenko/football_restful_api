from rest_framework.exceptions import NotFound

from .models import User


def get_user(id: int | None = None, email: str | None = None) -> User:
    if id:
        try:
            user = User.objects.get(id=id)
        except:
            raise NotFound(detail='User with given id does not exist.')

    elif email:
        try:
            user = User.objects.get(email=email)
        except:
            raise NotFound(detail='User with given email does not exist.')
    return user
