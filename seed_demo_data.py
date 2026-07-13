"""
StreamShield AI demo-data generator.

Run from the backend directory:

    python seed_demo_data.py

This script:
- Clears existing demo data
- Creates 12 streams
- Creates 6 metrics per stream
- Creates realistic incidents and recommendations
- Registers the existing knowledge-base runbooks
"""

from __future__ import annotations

import os
import random
from datetime import timedelta
from pathlib import Path
from typing import Any

import django


# -------------------------------------------------------------------
# Django setup
# -------------------------------------------------------------------

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()


from django.db import transaction  # noqa: E402
from django.utils import timezone  # noqa: E402

from streams.models import Stream, StreamMetric  # noqa: E402
from incidents.models import Incident, Recommendation  # noqa: E402

# KnowledgeDocument may be inside knowledge_base.models in the new structure.
# The fallback supports your previous model location.
try:
    from knowledge_base.models import KnowledgeDocument  # type: ignore # noqa: E402
except ImportError:
    from incidents.models import KnowledgeDocument  # type: ignore # noqa: E402


# -------------------------------------------------------------------
# Configuration
# -------------------------------------------------------------------

random.seed(42)

BASE_DIR = Path(__file__).resolve().parent
NOW = timezone.now()

METRICS_PER_STREAM = 6


STREAM_DEFINITIONS: list[dict[str, Any]] = [
    {
        "name": "World Cup Live",
        "event_name": "FIFA World Cup 2026 Final",
        "stream_url": "https://demo.streamshield.ai/world-cup",
        "region": "Germany-West",
        "status": "healthy",
        "expected_viewers": 1_200_000,
    },
    {
        "name": "IPL Final",
        "event_name": "IPL 2026 Championship Final",
        "stream_url": "https://demo.streamshield.ai/ipl-final",
        "region": "India",
        "status": "critical",
        "expected_viewers": 850_000,
    },
    {
        "name": "Champions League",
        "event_name": "UEFA Champions League Final",
        "stream_url": "https://demo.streamshield.ai/ucl-final",
        "region": "France-North",
        "status": "degraded",
        "expected_viewers": 640_000,
    },
    {
        "name": "NBA Finals",
        "event_name": "NBA Finals Game 7",
        "stream_url": "https://demo.streamshield.ai/nba-finals",
        "region": "USA-West",
        "status": "degraded",
        "expected_viewers": 720_000,
    },
    {
        "name": "UFC Main Event",
        "event_name": "UFC 320 Main Card",
        "stream_url": "https://demo.streamshield.ai/ufc-320",
        "region": "USA-East",
        "status": "healthy",
        "expected_viewers": 410_000,
    },
    {
        "name": "Wimbledon Final",
        "event_name": "Wimbledon Men's Final",
        "stream_url": "https://demo.streamshield.ai/wimbledon",
        "region": "UK-London",
        "status": "healthy",
        "expected_viewers": 525_000,
    },
    {
        "name": "Formula 1 Live",
        "event_name": "Monaco Grand Prix",
        "stream_url": "https://demo.streamshield.ai/f1-monaco",
        "region": "Monaco",
        "status": "healthy",
        "expected_viewers": 610_000,
    },
    {
        "name": "Olympics Live",
        "event_name": "Olympics Opening Ceremony",
        "stream_url": "https://demo.streamshield.ai/olympics",
        "region": "Japan-East",
        "status": "critical",
        "expected_viewers": 1_500_000,
    },
    {
        "name": "Asia Cup",
        "event_name": "Asia Cup Cricket Final",
        "stream_url": "https://demo.streamshield.ai/asia-cup",
        "region": "Singapore",
        "status": "healthy",
        "expected_viewers": 770_000,
    },
    {
        "name": "Valorant Masters",
        "event_name": "Valorant Masters Grand Final",
        "stream_url": "https://demo.streamshield.ai/valorant",
        "region": "South-Korea",
        "status": "degraded",
        "expected_viewers": 360_000,
    },
    {
        "name": "Copa America",
        "event_name": "Copa America Final",
        "stream_url": "https://demo.streamshield.ai/copa-america",
        "region": "Brazil-South",
        "status": "healthy",
        "expected_viewers": 930_000,
    },
    {
        "name": "Global Music Fest",
        "event_name": "Global Music Festival Live",
        "stream_url": "https://demo.streamshield.ai/music-festival",
        "region": "Australia-East",
        "status": "healthy",
        "expected_viewers": 290_000,
    },
]


METRIC_PROFILES: dict[str, dict[str, tuple[float, float]]] = {
    "healthy": {
        "viewer_ratio": (0.62, 0.88),
        "buffer_ratio": (0.2, 1.2),
        "startup_time_ms": (450, 1_200),
        "cdn_latency_ms": (35, 95),
        "failure_rate": (0.05, 0.6),
        "bitrate_kbps": (5_800, 8_200),
        "packet_loss": (0.01, 0.35),
        "fps": (55, 60),
    },
    "degraded": {
        "viewer_ratio": (0.68, 0.94),
        "buffer_ratio": (5.5, 15.0),
        "startup_time_ms": (2_200, 4_800),
        "cdn_latency_ms": (280, 850),
        "failure_rate": (3.0, 10.0),
        "bitrate_kbps": (2_200, 4_300),
        "packet_loss": (2.0, 7.0),
        "fps": (23, 34),
    },
    "critical": {
        "viewer_ratio": (0.72, 0.98),
        "buffer_ratio": (22.0, 42.0),
        "startup_time_ms": (6_000, 11_000),
        "cdn_latency_ms": (1_500, 3_200),
        "failure_rate": (18.0, 38.0),
        "bitrate_kbps": (550, 1_800),
        "packet_loss": (10.0, 22.0),
        "fps": (10, 20),
    },
}


INCIDENT_DEFINITIONS: list[dict[str, Any]] = [
    {
        "stream_name": "IPL Final",
        "title": "Major CDN Failure",
        "incident_type": "cdn_failure",
        "region": "India",
        "severity": "critical",
        "status": "investigating",
        "affected_users": 790_000,
        "probable_root_cause": (
            "The primary CDN edge cluster stopped responding while the "
            "viewer load was close to peak capacity."
        ),
        "ai_summary": (
            "A widespread increase in CDN latency and playback failures "
            "was detected across the India region. Traffic should be "
            "failed over to the secondary CDN immediately."
        ),
        "recommended_actions": [
            "Switch traffic to the secondary CDN",
            "Purge stale edge-cache entries",
            "Increase edge capacity in the India region",
            "Notify the CDN provider's network operations team",
        ],
        "confidence_score": 0.97,
        "minutes_ago": 8,
        "recommendations": [
            ("Fail over to the secondary CDN immediately", "critical"),
            ("Increase edge cache capacity", "high"),
            ("Open a priority case with the CDN provider", "high"),
        ],
    },
    {
        "stream_name": "Olympics Live",
        "title": "Regional Network Outage",
        "incident_type": "regional_outage",
        "region": "Japan-East",
        "severity": "critical",
        "status": "open",
        "affected_users": 1_120_000,
        "probable_root_cause": (
            "A network path failure between the origin and the Japan-East "
            "edge locations caused widespread stream interruption."
        ),
        "ai_summary": (
            "The Japan-East region is experiencing abnormal packet loss, "
            "high latency and playback failures consistent with a regional "
            "network disruption."
        ),
        "recommended_actions": [
            "Redirect viewers to the nearest healthy region",
            "Enable disaster-recovery routing",
            "Validate upstream transit-provider health",
            "Notify the regional network operations team",
        ],
        "confidence_score": 0.95,
        "minutes_ago": 18,
        "recommendations": [
            ("Redirect traffic to Singapore and South Korea", "critical"),
            ("Enable disaster-recovery routing", "critical"),
            ("Check upstream transit-provider status", "high"),
        ],
    },
    {
        "stream_name": "Champions League",
        "title": "Severe Buffering Spike",
        "incident_type": "buffering",
        "region": "France-North",
        "severity": "high",
        "status": "investigating",
        "affected_users": 284_000,
        "probable_root_cause": (
            "An unexpected viewer surge overloaded origin servers and "
            "reduced the available throughput for video segments."
        ),
        "ai_summary": (
            "Buffer ratio and startup delay rose sharply after concurrent "
            "viewership exceeded the expected operating level."
        ),
        "recommended_actions": [
            "Scale the origin-server pool",
            "Enable aggressive adaptive-bitrate switching",
            "Increase cache coverage for popular segments",
        ],
        "confidence_score": 0.92,
        "minutes_ago": 31,
        "recommendations": [
            ("Autoscale the origin cluster", "high"),
            ("Temporarily reduce the default video bitrate", "medium"),
            ("Increase segment-cache duration", "medium"),
        ],
    },
    {
        "stream_name": "NBA Finals",
        "title": "Origin Server Overload",
        "incident_type": "traffic_spike",
        "region": "USA-West",
        "severity": "high",
        "status": "open",
        "affected_users": 226_000,
        "probable_root_cause": (
            "The origin-server request rate exceeded configured autoscaling "
            "limits during a sudden viewer spike."
        ),
        "ai_summary": (
            "High startup latency and increased playback failures indicate "
            "that the origin tier is operating beyond its safe capacity."
        ),
        "recommended_actions": [
            "Increase origin autoscaling limits",
            "Warm the backup origin cluster",
            "Move popular content to edge cache",
        ],
        "confidence_score": 0.89,
        "minutes_ago": 46,
        "recommendations": [
            ("Increase origin autoscaling limits", "high"),
            ("Warm the standby origin cluster", "high"),
            ("Pre-cache high-demand segments", "medium"),
        ],
    },
    {
        "stream_name": "Valorant Masters",
        "title": "Packet Loss Degradation",
        "incident_type": "packet_loss",
        "region": "South-Korea",
        "severity": "medium",
        "status": "investigating",
        "affected_users": 94_000,
        "probable_root_cause": (
            "Packet loss increased on the regional route between the ingest "
            "gateway and the CDN edge network."
        ),
        "ai_summary": (
            "The stream remains available, but packet loss is causing lower "
            "frame rates, quality drops and intermittent buffering."
        ),
        "recommended_actions": [
            "Reroute traffic through the backup network path",
            "Check ingest gateway health",
            "Reduce the highest adaptive-bitrate profile",
        ],
        "confidence_score": 0.86,
        "minutes_ago": 64,
        "recommendations": [
            ("Reroute traffic through the backup network path", "high"),
            ("Validate the ingest gateway", "medium"),
            ("Temporarily cap the maximum bitrate", "medium"),
        ],
    },
    {
        "stream_name": "Global Music Fest",
        "title": "Playback Startup Delay",
        "incident_type": "playback_startup",
        "region": "Australia-East",
        "severity": "medium",
        "status": "resolved",
        "affected_users": 38_000,
        "probable_root_cause": (
            "A stale player-configuration response increased manifest "
            "resolution and playback startup time."
        ),
        "ai_summary": (
            "Startup delay briefly exceeded the recommended threshold. "
            "Cache invalidation restored normal startup performance."
        ),
        "recommended_actions": [
            "Invalidate player configuration cache",
            "Monitor manifest resolution time",
            "Review cache expiration settings",
        ],
        "confidence_score": 0.84,
        "minutes_ago": 92,
        "resolved_minutes_ago": 54,
        "recommendations": [
            ("Invalidate player-configuration cache", "medium"),
            ("Review cache-expiration configuration", "low"),
        ],
    },
    {
        "stream_name": "Wimbledon Final",
        "title": "Encoder Instability",
        "incident_type": "encoder_failure",
        "region": "UK-London",
        "severity": "high",
        "status": "resolved",
        "affected_users": 71_000,
        "probable_root_cause": (
            "The primary video encoder produced unstable output after a "
            "temporary resource-exhaustion event."
        ),
        "ai_summary": (
            "Frame rate and bitrate dropped briefly before traffic was "
            "switched to the standby encoder."
        ),
        "recommended_actions": [
            "Keep the standby encoder active",
            "Restart the primary encoder instance",
            "Review encoder CPU and memory limits",
        ],
        "confidence_score": 0.9,
        "minutes_ago": 135,
        "resolved_minutes_ago": 101,
        "recommendations": [
            ("Keep the standby encoder active", "high"),
            ("Restart and validate the primary encoder", "medium"),
            ("Increase encoder resource limits", "medium"),
        ],
    },
    {
        "stream_name": "Copa America",
        "title": "Transient Authentication Failures",
        "incident_type": "authentication_failure",
        "region": "Brazil-South",
        "severity": "low",
        "status": "resolved",
        "affected_users": 12_500,
        "probable_root_cause": (
            "A short-lived increase in token-validation latency caused "
            "a small percentage of playback authorization failures."
        ),
        "ai_summary": (
            "The authentication service recovered automatically. No ongoing "
            "viewer impact is currently detected."
        ),
        "recommended_actions": [
            "Monitor token-validation latency",
            "Review authentication-service connection limits",
            "Confirm retry policies in the player",
        ],
        "confidence_score": 0.78,
        "minutes_ago": 210,
        "resolved_minutes_ago": 184,
        "recommendations": [
            ("Monitor authentication latency", "low"),
            ("Review service connection limits", "low"),
        ],
    },
]


KNOWLEDGE_DOCUMENTS: list[dict[str, str]] = [
    {
        "title": "Buffering Troubleshooting Runbook",
        "document_type": "markdown",
        "file_path": "runbooks/buffering.md",
    },
    {
        "title": "CDN Failure Response Runbook",
        "document_type": "markdown",
        "file_path": "runbooks/cdn_failure.md",
    },
    {
        "title": "Traffic Spike Scaling Guide",
        "document_type": "markdown",
        "file_path": "runbooks/traffic_spike.md",
    },
    {
        "title": "Regional Outage Recovery SOP",
        "document_type": "markdown",
        "file_path": "runbooks/regional_outage.md",
    },
    {
        "title": "Playback Startup Troubleshooting Guide",
        "document_type": "markdown",
        "file_path": "runbooks/playback_startup.md",
    },
]


# -------------------------------------------------------------------
# Utility functions
# -------------------------------------------------------------------

def random_float(
    minimum: float,
    maximum: float,
    decimals: int = 2,
) -> float:
    return round(random.uniform(minimum, maximum), decimals)


def random_integer(minimum: float, maximum: float) -> int:
    return int(random.uniform(minimum, maximum))


def profile_value(
    status: str,
    field: str,
    decimals: int = 2,
) -> float:
    minimum, maximum = METRIC_PROFILES[status][field]
    return random_float(minimum, maximum, decimals)


def create_metric(
    *,
    stream: Stream,
    status: str,
    minutes_ago: int,
    sequence: int,
) -> StreamMetric:
    """
    Create one metric and move its timestamp into the past.

    queryset.update() is used so this also works when timestamp uses
    auto_now_add=True.
    """

    profile = METRIC_PROFILES[status]

    viewer_ratio = random_float(
        *profile["viewer_ratio"],
        decimals=3,
    )

    concurrent_viewers = int(
        stream.expected_viewers * viewer_ratio,
    )

    # Make recent critical/degraded points slightly worse so charts
    # visually show a rising incident.
    recent_pressure = sequence / max(METRICS_PER_STREAM - 1, 1)

    buffer_ratio = profile_value(
        status,
        "buffer_ratio",
    )

    cdn_latency = profile_value(
        status,
        "cdn_latency_ms",
    )

    failure_rate = profile_value(
        status,
        "failure_rate",
    )

    if status == "degraded":
        buffer_ratio += recent_pressure * 2.5
        cdn_latency += recent_pressure * 100
        failure_rate += recent_pressure * 1.5

    if status == "critical":
        buffer_ratio += recent_pressure * 5
        cdn_latency += recent_pressure * 350
        failure_rate += recent_pressure * 4

    metric = StreamMetric.objects.create(
        stream=stream,
        region=stream.region,
        concurrent_viewers=concurrent_viewers,
        buffer_ratio=round(buffer_ratio, 2),
        startup_time_ms=random_integer(
            *profile["startup_time_ms"],
        ),
        cdn_latency_ms=round(cdn_latency, 2),
        failure_rate=round(failure_rate, 2),
        bitrate_kbps=random_integer(
            *profile["bitrate_kbps"],
        ),
        packet_loss=profile_value(
            status,
            "packet_loss",
        ),
        fps=random_integer(
            *profile["fps"],
        ),
        is_anomaly=status in {"degraded", "critical"},
    )

    metric_timestamp = NOW - timedelta(
        minutes=minutes_ago,
    )

    StreamMetric.objects.filter(
        pk=metric.pk,
    ).update(timestamp=metric_timestamp)

    return metric


def clear_existing_data() -> None:
    print("Clearing existing data...")

    Recommendation.objects.all().delete()
    Incident.objects.all().delete()
    StreamMetric.objects.all().delete()
    KnowledgeDocument.objects.all().delete()
    Stream.objects.all().delete()


def create_streams() -> dict[str, Stream]:
    print("Creating streams...")

    streams: dict[str, Stream] = {}

    for stream_data in STREAM_DEFINITIONS:
        stream = Stream.objects.create(**stream_data)
        streams[stream.name] = stream

    return streams


def create_metrics(
    streams: dict[str, Stream],
) -> int:
    print("Creating time-series metrics...")

    metric_count = 0

    for stream in streams.values():
        for index in range(METRICS_PER_STREAM):
            # Oldest metric is roughly 25 minutes ago;
            # newest is at the current time.
            minutes_ago = (
                METRICS_PER_STREAM - index - 1
            ) * 5

            create_metric(
                stream=stream,
                status=stream.status,
                minutes_ago=minutes_ago,
                sequence=index,
            )

            metric_count += 1

    return metric_count


def create_incidents(
    streams: dict[str, Stream],
) -> tuple[int, int]:
    print("Creating incidents and recommendations...")

    incident_count = 0
    recommendation_count = 0

    for incident_data in INCIDENT_DEFINITIONS:
        stream_name = incident_data["stream_name"]
        stream = streams[stream_name]

        recommendations = incident_data.pop(
            "recommendations",
        )

        minutes_ago = incident_data.pop(
            "minutes_ago",
        )

        resolved_minutes_ago = incident_data.pop(
            "resolved_minutes_ago",
            None,
        )

        incident = Incident.objects.create(
            stream=stream,
            **incident_data,
        )

        created_at = NOW - timedelta(
            minutes=minutes_ago,
        )

        update_fields: dict[str, Any] = {
            "created_at": created_at,
        }

        if resolved_minutes_ago is not None:
            update_fields["resolved_at"] = (
                NOW
                - timedelta(
                    minutes=resolved_minutes_ago,
                )
            )

        Incident.objects.filter(
            pk=incident.pk,
        ).update(**update_fields)

        for action, priority in recommendations:
            Recommendation.objects.create(
                incident=incident,
                action=action,
                priority=priority,
            )

            recommendation_count += 1

        incident_count += 1

    return incident_count, recommendation_count


def create_knowledge_documents() -> int:
    print("Registering knowledge-base documents...")

    created_count = 0

    for document_data in KNOWLEDGE_DOCUMENTS:
        KnowledgeDocument.objects.create(
            **document_data,
        )
        created_count += 1

    return created_count


# -------------------------------------------------------------------
# Main execution
# -------------------------------------------------------------------

@transaction.atomic
def seed_demo_data() -> None:
    clear_existing_data()

    streams = create_streams()
    metric_count = create_metrics(streams)

    incident_count, recommendation_count = (
        create_incidents(streams)
    )

    knowledge_document_count = (
        create_knowledge_documents()
    )

    print()
    print("=" * 60)
    print("StreamShield AI demo data inserted successfully")
    print("=" * 60)
    print(f"Streams:             {len(streams)}")
    print(f"Metrics:             {metric_count}")
    print(f"Incidents:           {incident_count}")
    print(f"Recommendations:     {recommendation_count}")
    print(
        f"Knowledge documents: {knowledge_document_count}",
    )
    print("=" * 60)
    print()
    print("Start Django:")
    print("  python manage.py runserver")
    print()
    print("Start frontend:")
    print("  npm run dev")
    print()


if __name__ == "__main__":
    seed_demo_data()