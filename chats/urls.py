from django.urls import path

from . import views


app_name = 'chats'

urlpatterns = [
    path('start/<int:user_id>/', views.StartChatView.as_view(), name='start'),
    path('<slug:chat_id>/', views.GetChatView.as_view(), name='detail'),
]