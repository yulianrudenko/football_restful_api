from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from authentication.selectors import get_user
from .services import start_chat
from .selectors import get_chat
from .serializers import ChatSerializer


class StartChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        with_user = get_user(id=user_id)
        new_chat_id = start_chat(user1=request.user, user2=with_user)
        return Response({'chat_id': new_chat_id}, status=status.HTTP_201_CREATED)


class GetChatView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, chat_id):
        chat = get_chat(id=chat_id)

        if not request.user in chat.users.all():
            raise PermissionDenied(detail='You are not chat member')
            
        chat_serializer = ChatSerializer(chat)
        return Response(chat_serializer.data, status=status.HTTP_200_OK)