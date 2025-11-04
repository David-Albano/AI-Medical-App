from django.db import models

class KnowledgeChunk(models.Model):
    """Stored documents for RAG (embedded medical info)"""
    title = models.CharField(max_length=255)
    content = models.TextField()
    embedding = models.JSONField()  # store vector as list of floats
    source = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.title


class ChatSession(models.Model):
    """Conversation context"""
    session_id = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Session {self.session_id}"


class ChatMessage(models.Model):
    """User & AI messages"""
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name="messages")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
