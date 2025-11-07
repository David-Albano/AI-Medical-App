from django.db import models

class GuidelineDocument(models.Model):
    """Medical guideline or insurance policy text"""
    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='guidelines/')
    content = models.TextField(blank=True, null=True)
    embedding = models.JSONField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    processed = models.BooleanField(default=False)  # to track if embeddings were created

    def __str__(self):
        return self.title
    

class GuidelineChunk(models.Model):
    """Smaller section of a guideline for RAG retrieval"""
    guideline = models.ForeignKey(GuidelineDocument, on_delete=models.CASCADE, related_name="chunks")
    content = models.TextField()
    embedding = models.JSONField(blank=True, null=True)
    order = models.IntegerField(default=0)


class ComparisonQuery(models.Model):
    """User queries comparing a case against a policy"""
    query_text = models.TextField()
    guideline = models.ForeignKey(GuidelineDocument, on_delete=models.CASCADE, related_name="queries")
    ai_response = models.TextField(blank=True, null=True)
    verdict = models.CharField(max_length=50, blank=True, null=True)  # "Covered", "Not covered", etc.
    confidence = models.FloatField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
