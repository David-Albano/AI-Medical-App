from django.db import models

class MedicalDocument(models.Model):
    """Uploaded medical report or image"""
    DOC_TYPES = [
        ('pdf', 'PDF'),
        ('image', 'Image'),
        ('text', 'Text File'),
    ]
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='uploads/')
    doc_type = models.CharField(max_length=20, choices=DOC_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    extracted_text = models.TextField(blank=True, null=True)
    analyzed_summary = models.TextField(blank=True, null=True)
    findings_json = models.JSONField(blank=True, null=True)  # structured fields

    def __str__(self):
        return self.name
