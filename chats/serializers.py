from rest_framework import serializers
from .models import Chat, Message


class MessageSerializer(serializers.Serializer):
    user = serializers.CharField()
    text = serializers.CharField()


class ChatSerializer(serializers.ModelSerializer):
    messages = MessageSerializer(many=True, read_only=True)

    class Meta:
        model = Chat
        fields = ['users', 'messages']
