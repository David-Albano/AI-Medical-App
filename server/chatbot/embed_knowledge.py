# chatbot/management/commands/embed_knowledge.py
from django.core.management.base import BaseCommand
from models import KnowledgeChunk
from rag_utils import get_embedding

class Command(BaseCommand):
    help = "Generate embeddings for KnowledgeChunks"

    def handle(self, *args, **kwargs):
        chunks = KnowledgeChunk.objects.filter(embedding__isnull=True)
        for c in chunks:
            c.embedding = get_embedding(c.content)
            c.save()
            self.stdout.write(self.style.SUCCESS(f"Embedded: {c.title}"))
