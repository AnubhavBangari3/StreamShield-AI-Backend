from rest_framework import serializers

from .models import Stream, StreamMetric


class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = "__all__"


class StreamMetricSerializer(serializers.ModelSerializer):
    stream_name = serializers.CharField(
        source="stream.name",
        read_only=True,
    )

    class Meta:
        model = StreamMetric
        fields = "__all__"
        read_only_fields = [
            "timestamp",
            "is_anomaly",
        ]