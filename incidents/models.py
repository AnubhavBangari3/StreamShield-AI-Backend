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
    recommended_actions = models.JSONField(default=list, blank=True)
    confidence_score = models.FloatField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title