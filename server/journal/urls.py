from django.urls import path
from . import views

urlpatterns = [
    path("journal-entry/", views.JournalEntryView.as_view(), name="JournalEntryView"),
    path('sentiment-over-time/', views.sentiment_over_time, name='sentiment-over-time'),
    path('emotion-proportion/', views.emotion_proportion, name='emotion-proportion'),
    path('daily-journal-activity/', views.daily_journal_activity, name='daily-journal-activity'),
]