from django.db import models


class Stream(models.Model):
    STATUS_CHOICES = [
        ("healthy", "Healthy"),
        ("degraded", "Degraded"),
        ("critical", "Critical"),
    ]

    name = models.CharField(max_length=200)
    event_name = models.CharField(max_length=200)
    stream_url = models.URLField(blank=True)

    region = models.CharField(
        max_length=100,
        default="Europe",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="healthy",
    )

    expected_viewers = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class StreamMetric(models.Model):
    stream = models.ForeignKey(
        Stream,
        on_delete=models.CASCADE,
        related_name="metrics",
    )

    timestamp = models.DateTimeField(auto_now_add=True)

    region = models.CharField(max_length=100)

    concurrent_viewers = models.PositiveIntegerField(default=0)

    buffer_ratio = models.FloatField(default=0)

    startup_time_ms = models.FloatField(default=0)

    cdn_latency_ms = models.FloatField(default=0)

    failure_rate = models.FloatField(default=0)

    bitrate_kbps = models.FloatField(default=0)

    packet_loss = models.FloatField(default=0)

    fps = models.FloatField(default=30)

    is_anomaly = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.stream.name} - {self.timestamp}"