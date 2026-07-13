from rest_framework import serializers

from streams.models import Stream


class SimulationRequestSerializer(serializers.Serializer):
    SCENARIO_CHOICES = [
        ("normal", "Normal Traffic"),
        ("traffic_spike", "Traffic Spike"),
        ("buffering_spike", "Buffering Spike"),
        ("cdn_failure", "CDN Failure"),
        ("regional_outage", "Regional Outage"),
    ]

    scenario = serializers.ChoiceField(
        choices=SCENARIO_CHOICES,
    )

    stream_id = serializers.PrimaryKeyRelatedField(
        queryset=Stream.objects.all(),
        source="stream",
        required=False,
    )

    points = serializers.IntegerField(
        default=1,
        min_value=1,
        max_value=30,
    )