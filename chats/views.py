from django.shortcuts import render


def index(request):
    return render(request, 'chats/index.html')


def chat_room(request, room_name):
    return render(request, 'chats/chatroom.html', {'room_name': room_name})
