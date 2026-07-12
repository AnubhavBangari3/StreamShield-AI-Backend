from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Stream, StreamMetric
from .serializers import StreamMetricSerializer, StreamSerializer
from .services import create_incident_from_metric, detect_anomaly


class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all().order_by("-created_at")
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


class StreamMetricViewSet(viewsets.ModelViewSet):
    queryset = StreamMetric.objects.select_related("stream").all()
    serializer_class = StreamMetricSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        metric = serializer.save()

        is_anomaly, reason = detect_anomaly(metric)

        incident = None

        if is_anomaly:
            metric.is_anomaly = True
            metric.save(update_fields=["is_anomaly"])

            metric.stream.status = "critical"
            metric.stream.save(update_fields=["status"])

            incident = create_incident_from_metric(
                metric,
                reason,
            )

        response_data = {
            "metric": self.get_serializer(metric).data,
            "anomaly_detected": is_anomaly,
            "reason": reason,
            "incident_id": incident.id if incident else None,
        }

        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
        )