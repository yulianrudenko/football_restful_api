from django.db import transaction

from .models import User
from .utlis import send_activation_email


@transaction.atomic
def create_user(*, email: str, username: str) -> User:
    new_user = User.objects.create(
        email=email,
        username=username
    )
    send_activation_email(to_user=new_user)
    return new_user
