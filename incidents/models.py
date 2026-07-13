from django.db import models

from streams.models import Stream


class Incident(models.Model):
    SEVERITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("open", "Open"),
        ("investigating", "Investigating"),
        ("resolved", "Resolved"),
    ]

    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE,
        related_name="incidents",
    )

    title = models.CharField(max_length=255)

    incident_type = models.CharField(
        max_length=100,
        default="Streaming Issue",
    )

    region = models.CharField(max_length=100)

    severity = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="open",
    )

    affected_users = models.PositiveIntegerField(default=0)
    probable_root_cause = models.TextField(blank=True)
    ai_summary = models.TextField(blank=True)

    recommended_actions = models.JSONField(
        default=list,
        blank=True,
    )

    confidence_score = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title


class Recommendation(models.Model):
    PRIORITY_CHOICES = [
        ("low", "Low"),
        ("medium", "Medium"),
        ("high", "High"),
        ("critical", "Critical"),
    ]

    incident = models.ForeignKey(
        Incident,
        on_delete=models.CASCADE,
        related_name="recommendations",
    )

    action = models.TextField()

    priority = models.CharField(
        max_length=20,
        choices=PRIORITY_CHOICES,
        default="medium",
    )

    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.action


class KnowledgeDocument(models.Model):
    title = models.CharField(max_length=255)
    document_type = models.CharField(max_length=50)
    file_path = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-uploaded_at"]

    def __str__(self):
        return self.title