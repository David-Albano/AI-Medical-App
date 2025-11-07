from django.urls import path
from . import views

urlpatterns = [
    path("upload-guideline/", views.GuidelineUploadAPIView.as_view(), name="GuidelineUploadAPIView"),
    path("compare/<int:pk>/", views.CompareQueryAPIView.as_view(), name="CompareQueryAPIView"),
]