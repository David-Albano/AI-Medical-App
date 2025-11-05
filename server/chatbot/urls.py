from django.urls import path
from . import views

urlpatterns = [
    path('get-medical-categories/', views.GetMedicalCategories.as_view(), name='GetMedicalCategories'),
    path('upload-knowledge/', views.upload_knowledge_files, name='upload_knowledge'),
    path('chat/', views.ChatbotAPIView.as_view(), name='ChatbotAPIView'),
    path('chat/<int:session_pk>/', views.ChatbotAPIView.as_view(), name='ChatbotSessionAPIView'),
]