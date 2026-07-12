from rest_framework import serializers

from .models import Incident


class IncidentSerializer(serializers.ModelSerializer):
    stream_name = serializers.CharField(
        source="stream.name",
        read_only=True,
    )

    class Meta:
        model = Incident
        fields = "__all__"
        read_only_fields = [
            "created_at",
            "resolved_at",
        ]