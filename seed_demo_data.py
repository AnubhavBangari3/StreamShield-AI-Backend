from streams.models import Stream, StreamMetric
from incidents.models import Incident, Recommendation, KnowledgeDocument

# Clear existing data
Recommendation.objects.all().delete()
Incident.objects.all().delete()
StreamMetric.objects.all().delete()
KnowledgeDocument.objects.all().delete()
Stream.objects.all().delete()

# ------------------------
# Streams
# ------------------------

s1 = Stream.objects.create(
    name="World Cup Live",
    event_name="FIFA World Cup 2026",
    stream_url="https://demo.com/worldcup",
    region="Germany-West",
    status="healthy",
    expected_viewers=1200000,
)

s2 = Stream.objects.create(
    name="IPL Final",
    event_name="IPL 2026 Final",
    stream_url="https://demo.com/ipl",
    region="India",
    status="critical",
    expected_viewers=850000,
)

s3 = Stream.objects.create(
    name="Champions League",
    event_name="UCL Final",
    stream_url="https://demo.com/ucl",
    region="France-North",
    status="degraded",
    expected_viewers=640000,
)

# ------------------------
# Metrics
# ------------------------

StreamMetric.objects.create(
    stream=s1,
    region="Germany-West",
    concurrent_viewers=980000,
    buffer_ratio=0.8,
    startup_time_ms=900,
    cdn_latency_ms=60,
    failure_rate=0.2,
    bitrate_kbps=7200,
    packet_loss=0.1,
    fps=60,
    is_anomaly=False,
)

StreamMetric.objects.create(
    stream=s2,
    region="India",
    concurrent_viewers=830000,
    buffer_ratio=35,
    startup_time_ms=8500,
    cdn_latency_ms=2400,
    failure_rate=28,
    bitrate_kbps=900,
    packet_loss=16,
    fps=15,
    is_anomaly=True,
)

StreamMetric.objects.create(
    stream=s3,
    region="France-North",
    concurrent_viewers=540000,
    buffer_ratio=12,
    startup_time_ms=3200,
    cdn_latency_ms=640,
    failure_rate=8,
    bitrate_kbps=3100,
    packet_loss=5,
    fps=28,
    is_anomaly=True,
)

# ------------------------
# Incidents
# ------------------------

i1 = Incident.objects.create(
    stream=s2,
    title="Major CDN Failure",
    incident_type="CDN Failure",
    region="India",
    severity="critical",
    status="investigating",
    affected_users=790000,
    probable_root_cause="Primary CDN node failure",
    ai_summary="AI detected widespread CDN latency affecting playback.",
    recommended_actions=[
        "Switch traffic to backup CDN",
        "Purge CDN cache",
        "Increase edge capacity",
    ],
    confidence_score=0.96,
)

i2 = Incident.objects.create(
    stream=s3,
    title="Buffering Spike",
    incident_type="Buffering",
    region="France-North",
    severity="high",
    status="open",
    affected_users=280000,
    probable_root_cause="Unexpected traffic surge",
    ai_summary="High buffering caused by overloaded origin servers.",
    recommended_actions=[
        "Scale origin servers",
        "Enable adaptive bitrate",
    ],
    confidence_score=0.91,
)

# ------------------------
# Recommendations
# ------------------------

Recommendation.objects.create(
    incident=i1,
    action="Fail over to secondary CDN immediately",
    priority="critical",
)

Recommendation.objects.create(
    incident=i1,
    action="Increase edge cache TTL",
    priority="high",
)

Recommendation.objects.create(
    incident=i2,
    action="Autoscale origin cluster",
    priority="high",
)

Recommendation.objects.create(
    incident=i2,
    action="Reduce video bitrate temporarily",
    priority="medium",
)

# ------------------------
# Knowledge Base
# ------------------------

KnowledgeDocument.objects.create(
    title="CDN Failure Runbook",
    document_type="markdown",
    file_path="runbooks/cdn_failure.md",
)

KnowledgeDocument.objects.create(
    title="Buffering Troubleshooting Guide",
    document_type="pdf",
    file_path="runbooks/buffering.pdf",
)

KnowledgeDocument.objects.create(
    title="Regional Outage SOP",
    document_type="markdown",
    file_path="runbooks/regional_outage.md",
)

print("Demo data inserted successfully.")