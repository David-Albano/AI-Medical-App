from django.urls import path
from . import views

urlpatterns = [
    path('chat/', views.ChatbotAPIView.as_view(), name='chat'),
    path('chat/<int:session_pk>/', views.ChatbotAPIView.as_view(), name='chat-session'),
]