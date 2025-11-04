from django.db import models

class GuidelineDocument(models.Model):
    """Medical guideline or insurance policy text"""
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='guidelines/')
    content = models.TextField(blank=True, null=True)
    embedding = models.JSONField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class ComparisonQuery(models.Model):
    """User queries comparing a case against a policy"""
    query_text = models.TextField()
    guideline = models.ForeignKey(GuidelineDocument, on_delete=models.CASCADE, related_name="queries")
    ai_response = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
