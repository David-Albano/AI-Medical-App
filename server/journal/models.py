from django.db import models

class JournalEntry(models.Model):
    """Daily journal or mood entry"""
    date = models.DateField(auto_now_add=True)
    text = models.TextField()
    sentiment = models.CharField(max_length=20, blank=True, null=True)  # e.g., positive, negative
    emotion = models.CharField(max_length=50, blank=True, null=True)    # e.g., sad, anxious
    ai_feedback = models.TextField(blank=True, null=True)               # AI-generated tip

    def __str__(self):
        return f"Entry {self.date} - {self.sentiment or 'Unanalyzed'}"
