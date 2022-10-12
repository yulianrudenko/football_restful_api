import uuid
from django.db import models

from authentication.models import User


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    users = models.ManyToManyField(to=User, related_name='chats')

    class Meta:
        ordering = ['id']

    def __str__(self) -> str:
        return str(self.id)  


class Message(models.Model):
    chat = models.ForeignKey(to=Chat, related_name='messages', on_delete=models.CASCADE)
    user = models.ForeignKey(to=User, related_name='messages', on_delete=models.SET_NULL, null=True)
    text = models.CharField(max_length=325, blank=False)
    date_sent = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        ordering = ['date_sent', 'user']

    def __str__(self) -> str:
        return 'Message by ' + self.user.email + ' at ' + self.date_sent.strftime("%H:%M:%S %y.%m.%d")

    def clean(self) -> None:
        if self.user not in self.chat.users.all():
            raise ValueError({'user', 'User sending message is not chat participant'})

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)
