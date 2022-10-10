from django.urls import path

from . import views


app_name = 'chats'

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:room_name>/', views.chat_room, name='chat-room'),
]