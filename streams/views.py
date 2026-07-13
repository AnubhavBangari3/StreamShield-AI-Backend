from django.db.models import Avg, Sum
from rest_framework import status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.response import Response

from incidents.models import Incident

from .models import Stream, StreamMetric
from .serializers import StreamMetricSerializer, StreamSerializer
from .services import create_incident_from_metric, detect_anomaly


class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.order_by("-created_at")
    serializer_class = StreamSerializer

    @action(detail=True, methods=["get"])
    def metrics(self, request, pk=None):
        stream = self.get_object()
        metrics = stream.metrics.all()[:50]

        serializer = StreamMetricSerializer(
            metrics,
            many=True,
        )

        return Response(serializer.data)

    @action(detail=True, methods=["get"])
    def incidents(self, request, pk=None):
        from incidents.serializers import IncidentSerializer

        stream = self.get_object()
        incidents = stream.incidents.all()[:20]

        serializer = IncidentSerializer(
            incidents,
            many=True,
        )

        return Response(serializer.data)


class StreamMetricViewSet(viewsets.ModelViewSet):
    queryset = (
        StreamMetric.objects
        .select_related("stream")
        .order_by("-timestamp")[:100]
    )
    serializer_class = StreamMetricSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        metric = serializer.save()

        is_anomaly, reasons = detect_anomaly(metric)
        incident = None

        if is_anomaly:
            metric.is_anomaly = True
            metric.save(update_fields=["is_anomaly"])

            metric.stream.status = "critical"
            metric.stream.save(update_fields=["status"])

            incident = create_incident_from_metric(
                metric=metric,
                reasons=reasons,
            )

        response_data = {
            "metric": self.get_serializer(metric).data,
            "anomaly_detected": is_anomaly,
            "reasons": reasons,
            "incident_id": incident.id if incident else None,
        }

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
        )


@api_view(["GET"])
def dashboard_summary(request):
    streams = Stream.objects.all()
    metrics = StreamMetric.objects.all()
    incidents = Incident.objects.all()

    metric_summary = metrics.aggregate(
        total_viewers=Sum("concurrent_viewers"),
        average_latency=Avg("cdn_latency_ms"),
        average_buffer_ratio=Avg("buffer_ratio"),
        average_failure_rate=Avg("failure_rate"),
    )

    data = {
        "total_streams": streams.count(),
        "healthy_streams": streams.filter(status="healthy").count(),
        "degraded_streams": streams.filter(status="degraded").count(),
        "critical_streams": streams.filter(status="critical").count(),
        "active_incidents": incidents.exclude(status="resolved").count(),
        "critical_incidents": incidents.filter(
            severity="critical",
            status__in=["open", "investigating"],
        ).count(),
        "total_viewers": metric_summary["total_viewers"] or 0,
        "average_latency": round(
            metric_summary["average_latency"] or 0,
            2,
        ),
        "average_buffer_ratio": round(
            metric_summary["average_buffer_ratio"] or 0,
            2,
        ),
        "average_failure_rate": round(
            metric_summary["average_failure_rate"] or 0,
            2,
        ),
    }

    return Response(data)