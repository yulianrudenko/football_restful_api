from rest_framework import serializers
from .models import Chat, Message


class MessageSerializer(serializers.Serializer):
    user = serializers.CharField(source="user.username")
    text = serializers.CharField()
    date_sent = serializers.DateTimeField(format='%H:%M:%S %y.%m.%d')


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['users', 'messages']
