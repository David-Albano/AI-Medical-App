from django.db import models

class HealthMetric(models.Model):
    """Mock daily vitals data for reasoning"""
    date = models.DateField(auto_now_add=True)
    heart_rate = models.IntegerField(blank=True, null=True)
    sleep_hours = models.FloatField(blank=True, null=True)
    glucose_level = models.FloatField(blank=True, null=True)

    def __str__(self):
        return f"Metrics {self.date}"


class AISuggestion(models.Model):
    """Agent-generated personalized suggestions"""
    created_at = models.DateTimeField(auto_now_add=True)
    context_summary = models.TextField(blank=True, null=True)  # reasoning context
    suggestion_text = models.TextField()
    status = models.CharField(max_length=20, default='new')  # new / applied / ignored

    def __str__(self):
        return f"Suggestion {self.id} - {self.status}"
