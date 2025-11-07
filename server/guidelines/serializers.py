# guidelines/serializers.py
from rest_framework import serializers
from .models import GuidelineDocument, GuidelineChunk, ComparisonQuery

class GuidelineDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuidelineDocument
        fields = ["id", "title", "file", "content", "processed", "uploaded_at"]

class GuidelineChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = GuidelineChunk
        fields = ["id", "guideline", "content", "order"]

class ComparisonQuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComparisonQuery
        fields = ["id", "query_text", "guideline", "ai_response", "verdict", "confidence", "created_at"]
        read_only_fields = ["ai_response", "verdict", "confidence", "created_at"]
