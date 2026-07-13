from incidents.models import Incident, Recommendation

from .models import StreamMetric


def detect_anomaly(metric: StreamMetric) -> tuple[bool, list[str]]:
    reasons = []

    if metric.buffer_ratio >= 10:
        reasons.append("High buffering ratio")

    if metric.cdn_latency_ms >= 700:
        reasons.append("High CDN latency")

    if metric.failure_rate >= 8:
        reasons.append("High stream failure rate")

    if metric.startup_time_ms >= 5000:
        reasons.append("Slow stream startup time")

    if metric.packet_loss >= 5:
        reasons.append("High packet loss")

    if metric.fps < 24:
        reasons.append("Low frame rate")

    return bool(reasons), reasons


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

    if metric.packet_loss >= 10:
        score += 3
    elif metric.packet_loss >= 5:
        score += 2

    if score >= 8:
        return "critical"

    if score >= 5:
        return "high"

    if score >= 3:
        return "medium"

    return "low"


def determine_incident_type(reasons: list[str]) -> str:
    reason_text = " ".join(reasons).lower()

    if "cdn latency" in reason_text:
        return "CDN Degradation"

    if "buffering" in reason_text:
        return "Buffering Issue"

    if "failure rate" in reason_text:
        return "Stream Failure"

    if "packet loss" in reason_text:
        return "Network Packet Loss"

    if "startup" in reason_text:
        return "Slow Playback Startup"

    if "frame rate" in reason_text:
        return "Video Quality Degradation"

    return "Streaming Issue"


def create_incident_from_metric(
    metric: StreamMetric,
    reasons: list[str],
) -> Incident:
    severity = calculate_severity(metric)
    incident_type = determine_incident_type(reasons)

    affected_users = int(
        metric.concurrent_viewers
        * min(metric.failure_rate / 100, 1)
    )

    recommended_actions = [
        "Check CDN node health",
        "Review regional traffic load",
        "Route traffic to a healthy CDN region",
        "Temporarily reduce the maximum bitrate",
    ]

    incident = Incident.objects.create(
        stream=metric.stream,
        title=f"{severity.title()} {incident_type}",
        incident_type=incident_type,
        region=metric.region,
        severity=severity,
        affected_users=affected_users,
        probable_root_cause=", ".join(reasons),
        ai_summary=(
            f"{incident_type} detected in {metric.region}. "
            f"Evidence: {', '.join(reasons)}."
        ),
        recommended_actions=recommended_actions,
        confidence_score=0.75,
    )

    for action in recommended_actions:
        Recommendation.objects.create(
            incident=incident,
            action=action,
            priority=severity if severity != "low" else "medium",
        )

    return incident