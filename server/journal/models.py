from django.db import models

class JournalEntry(models.Model):
    """Daily journal or mood entry"""
    date = models.DateField(auto_now_add=True)
    text = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True, null=True)
    emotion = models.CharField(max_length=50, blank=True, null=True)
    sentiment_justification = models.TextField(blank=True, null=True)
    emotion_justification = models.TextField(blank=True, null=True)
    ai_feedback = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Entry {self.date} - {self.sentiment or 'Unanalyzed'}"
