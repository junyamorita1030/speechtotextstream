# chat/routing.py
from django.urls import path

from . import consumers


websocket_urlpatterns = [
    path('ws/stt_with_browser/<str:room_name>/', consumers.ChatConsumer),
]
