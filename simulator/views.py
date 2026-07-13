import random
from datetime import timedelta

from django.db import transaction
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from incidents.models import Incident
from incidents.serializers import IncidentSerializer
from streams.models import Stream, StreamMetric
from streams.serializers import StreamMetricSerializer
from streams.services import (
    create_incident_from_metric,
    detect_anomaly,
    determine_incident_type,
)

from .serializers import SimulationRequestSerializer


SCENARIO_LABELS = {
    "normal": "Normal Traffic",
    "traffic_spike": "Traffic Spike",
    "buffering_spike": "Buffering Spike",
    "cdn_failure": "CDN Failure",
    "regional_outage": "Regional Outage",
}


def get_or_create_default_stream() -> Stream:
    """
    Creates a default demo stream when stream_id is not supplied.
    """

    stream, _ = Stream.objects.get_or_create(
        name="World Cup Live Stream",
        defaults={
            "event_name": "FIFA World Cup 2026",
            "region": "Germany-West",
            "status": "healthy",
            "expected_viewers": 1_000_000,
            "stream_url": "",
        },
    )

    return stream


def generate_normal_metric(
    stream: Stream,
) -> dict:
    base_viewers = max(stream.expected_viewers, 100_000)

    return {
        "region": stream.region,
        "concurrent_viewers": random.randint(
            int(base_viewers * 0.65),
            int(base_viewers * 0.90),
        ),
        "buffer_ratio": round(
            random.uniform(0.2, 2.5),
            2,
        ),
        "startup_time_ms": round(
            random.uniform(500, 1800),
            2,
        ),
        "cdn_latency_ms": round(
            random.uniform(40, 180),
            2,
        ),
        "failure_rate": round(
            random.uniform(0.1, 1.5),
            2,
        ),
        "bitrate_kbps": round(
            random.uniform(4500, 8000),
            2,
        ),
        "packet_loss": round(
            random.uniform(0.1, 1.0),
            2,
        ),
        "fps": round(
            random.uniform(29, 60),
            2,
        ),
    }


def generate_traffic_spike_metric(
    stream: Stream,
) -> dict:
    base_viewers = max(stream.expected_viewers, 100_000)

    return {
        "region": stream.region,
        "concurrent_viewers": random.randint(
            int(base_viewers * 1.20),
            int(base_viewers * 1.80),
        ),
        "buffer_ratio": round(
            random.uniform(8, 14),
            2,
        ),
        "startup_time_ms": round(
            random.uniform(2800, 5500),
            2,
        ),
        "cdn_latency_ms": round(
            random.uniform(500, 850),
            2,
        ),
        "failure_rate": round(
            random.uniform(4, 9),
            2,
        ),
        "bitrate_kbps": round(
            random.uniform(2800, 5000),
            2,
        ),
        "packet_loss": round(
            random.uniform(2, 6),
            2,
        ),
        "fps": round(
            random.uniform(24, 30),
            2,
        ),
    }


def generate_buffering_spike_metric(
    stream: Stream,
) -> dict:
    base_viewers = max(stream.expected_viewers, 100_000)

    return {
        "region": stream.region,
        "concurrent_viewers": random.randint(
            int(base_viewers * 0.80),
            int(base_viewers * 1.10),
        ),
        "buffer_ratio": round(
            random.uniform(15, 30),
            2,
        ),
        "startup_time_ms": round(
            random.uniform(4500, 8500),
            2,
        ),
        "cdn_latency_ms": round(
            random.uniform(500, 950),
            2,
        ),
        "failure_rate": round(
            random.uniform(6, 14),
            2,
        ),
        "bitrate_kbps": round(
            random.uniform(1200, 3000),
            2,
        ),
        "packet_loss": round(
            random.uniform(4, 9),
            2,
        ),
        "fps": round(
            random.uniform(18, 26),
            2,
        ),
    }


def generate_cdn_failure_metric(
    stream: Stream,
) -> dict:
    base_viewers = max(stream.expected_viewers, 100_000)

    return {
        "region": stream.region,
        "concurrent_viewers": random.randint(
            int(base_viewers * 0.85),
            int(base_viewers * 1.20),
        ),
        "buffer_ratio": round(
            random.uniform(20, 40),
            2,
        ),
        "startup_time_ms": round(
            random.uniform(7000, 15000),
            2,
        ),
        "cdn_latency_ms": round(
            random.uniform(1000, 2500),
            2,
        ),
        "failure_rate": round(
            random.uniform(15, 35),
            2,
        ),
        "bitrate_kbps": round(
            random.uniform(500, 1800),
            2,
        ),
        "packet_loss": round(
            random.uniform(8, 18),
            2,
        ),
        "fps": round(
            random.uniform(10, 22),
            2,
        ),
    }


def generate_regional_outage_metric(
    stream: Stream,
) -> dict:
    base_viewers = max(stream.expected_viewers, 100_000)

    affected_regions = [
        "Germany-West",
        "Germany-Central",
        "France-North",
        "Netherlands-West",
        "Spain-Central",
    ]

    return {
        "region": random.choice(affected_regions),
        "concurrent_viewers": random.randint(
            int(base_viewers * 0.70),
            int(base_viewers * 1.10),
        ),
        "buffer_ratio": round(
            random.uniform(35, 70),
            2,
        ),
        "startup_time_ms": round(
            random.uniform(12000, 25000),
            2,
        ),
        "cdn_latency_ms": round(
            random.uniform(1800, 5000),
            2,
        ),
        "failure_rate": round(
            random.uniform(40, 90),
            2,
        ),
        "bitrate_kbps": round(
            random.uniform(0, 800),
            2,
        ),
        "packet_loss": round(
            random.uniform(20, 60),
            2,
        ),
        "fps": round(
            random.uniform(0, 15),
            2,
        ),
    }


SCENARIO_GENERATORS = {
    "normal": generate_normal_metric,
    "traffic_spike": generate_traffic_spike_metric,
    "buffering_spike": generate_buffering_spike_metric,
    "cdn_failure": generate_cdn_failure_metric,
    "regional_outage": generate_regional_outage_metric,
}


def update_stream_status(
    stream: Stream,
    anomaly_detected: bool,
    incident: Incident | None,
) -> None:
    if not anomaly_detected:
        new_status = "healthy"
    elif incident and incident.severity in ["high", "critical"]:
        new_status = "critical"
    else:
        new_status = "degraded"

    if stream.status != new_status:
        stream.status = new_status
        stream.save(update_fields=["status"])


def find_recent_related_incident(
    stream: Stream,
    incident_type: str,
    region: str,
) -> Incident | None:
    """
    Prevents a new incident from being created every three seconds
    for the same continuing problem.
    """

    two_minutes_ago = timezone.now() - timedelta(minutes=2)

    return (
        Incident.objects.filter(
            stream=stream,
            incident_type=incident_type,
            region=region,
            status__in=["open", "investigating"],
            created_at__gte=two_minutes_ago,
        )
        .order_by("-created_at")
        .first()
    )


@api_view(["GET"])
def scenario_list(request):
    return Response(
        {
            "scenarios": [
                {
                    "value": key,
                    "label": label,
                }
                for key, label in SCENARIO_LABELS.items()
            ]
        }
    )


@api_view(["POST"])
def generate_simulation(request):
    request_serializer = SimulationRequestSerializer(
        data=request.data
    )
    request_serializer.is_valid(raise_exception=True)

    validated_data = request_serializer.validated_data

    scenario = validated_data["scenario"]
    points = validated_data["points"]
    stream = validated_data.get(
        "stream",
        get_or_create_default_stream(),
    )

    metric_generator = SCENARIO_GENERATORS[scenario]

    generated_results = []

    for _ in range(points):
        with transaction.atomic():
            metric_values = metric_generator(stream)

            metric = StreamMetric.objects.create(
                stream=stream,
                **metric_values,
            )

            anomaly_detected, reasons = detect_anomaly(metric)

            incident = None
            incident_created = False

            if anomaly_detected:
                metric.is_anomaly = True
                metric.save(update_fields=["is_anomaly"])

                incident_type = determine_incident_type(reasons)

                incident = find_recent_related_incident(
                    stream=stream,
                    incident_type=incident_type,
                    region=metric.region,
                )

                if incident is None:
                    incident = create_incident_from_metric(
                        metric=metric,
                        reasons=reasons,
                    )
                    incident_created = True

            update_stream_status(
                stream=stream,
                anomaly_detected=anomaly_detected,
                incident=incident,
            )

            result = {
                "metric": StreamMetricSerializer(metric).data,
                "anomaly_detected": anomaly_detected,
                "reasons": reasons,
                "incident_created": incident_created,
                "incident": (
                    IncidentSerializer(incident).data
                    if incident
                    else None
                ),
            }

            generated_results.append(result)

    return Response(
        {
            "scenario": scenario,
            "scenario_label": SCENARIO_LABELS[scenario],
            "stream": {
                "id": stream.id,
                "name": stream.name,
                "status": stream.status,
                "region": stream.region,
            },
            "points_generated": len(generated_results),
            "results": generated_results,
        },
        status=status.HTTP_201_CREATED,
    )