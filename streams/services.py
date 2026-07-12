from incidents.models import Incident

from .models import StreamMetric


def detect_anomaly(metric: StreamMetric) -> tuple[bool, str]:
    reasons = []

    if metric.buffer_ratio >= 10:
        reasons.append("High buffering ratio")

    if metric.cdn_latency_ms >= 700:
        reasons.append("High CDN latency")

    if metric.failure_rate >= 8:
        reasons.append("High stream failure rate")

    if metric.startup_time_ms >= 5000:
        reasons.append("Slow stream startup")

    return bool(reasons), ", ".join(reasons)


def calculate_severity(metric: StreamMetric) -> str:
    score = 0

    if metric.buffer_ratio >= 20:
        score += 3
    elif metric.buffer_ratio >= 10:
        score += 2

    if metric.cdn_latency_ms >= 1000:
        score += 3
    elif metric.cdn_latency_ms >= 700:
        score += 2

    if metric.failure_rate >= 15:
        score += 3
    elif metric.failure_rate >= 8:
        score += 2

    if score >= 7:
        return "critical"

    if score >= 5:
        return "high"

    if score >= 3:
        return "medium"

    return "low"


def create_incident_from_metric(
    metric: StreamMetric,
    reason: str,
) -> Incident:
    severity = calculate_severity(metric)

    affected_users = int(
        metric.concurrent_viewers
        * min(metric.failure_rate / 100, 1)
    )

    return Incident.objects.create(
        stream=metric.stream,
        title=f"{severity.title()} streaming degradation",
        region=metric.region,
        severity=severity,
        affected_users=affected_users,
        probable_root_cause=reason,
        ai_summary=(
            f"Streaming quality degraded in {metric.region}. "
            f"Detected: {reason}."
        ),
        recommended_actions=[
            "Check CDN node health",
            "Review regional traffic load",
            "Temporarily reduce maximum bitrate",
            "Route traffic to a healthy CDN region",
        ],
        confidence_score=0.75,
    )