import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import Message
from .selectors import get_chat
from .serializers import MessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    def __create_message(self, user, message_text):
        chat = get_chat(id=self.chat_id)
        return Message.objects.create(
            chat=chat,
            user=user,
            text=message_text)

    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.room_group_name = 'chat_%s' % self.chat_id

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket (front)
    async def receive(self, text_data):
        user = self.scope['user']
        message_text = json.loads(text_data)['message']

        # insert message into db 
        message = await database_sync_to_async(
            self.__create_message)(user, message_text)

        message = MessageSerializer(message).data

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'new_message', 'message': message}
        )

    # Receive new message from room group
    async def new_message(self, event):
        message = event['message']

        # Send message to WebSocket (front)
        await self.send(text_data=json.dumps({
            'message': message,
        }))
