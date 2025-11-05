from django.urls import path
from . import views

urlpatterns = [
    path("journal-entry/", views.JournalEntryView.as_view(), name="JournalEntryView"),
]