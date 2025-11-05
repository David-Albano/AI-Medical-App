from django.urls import path
from . import views

urlpatterns = [
    path('upload-knowledge/', views.upload_knowledge_files, name='upload_knowledge'),
    path('chat/', views.ChatbotAPIView.as_view(), name='chat'),
    path('chat/<int:session_pk>/', views.ChatbotAPIView.as_view(), name='chat_session'),
]