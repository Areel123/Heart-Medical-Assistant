from django.urls import path
from .views import chat_api, home

urlpatterns = [
    path("", home),          # http://127.0.0.1:8000/
    path("chat/", chat_api), # http://127.0.0.1:8000/api/chat/
]