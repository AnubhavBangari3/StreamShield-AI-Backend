from rest_framework import serializers

from .models import (
    Incident,
    Recommendation,
    KnowledgeDocument,
)


class RecommendationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recommendation
        fields = "__all__"


class KnowledgeDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = KnowledgeDocument
        fields = "__all__"


class IncidentSerializer(serializers.ModelSerializer):
    stream_name = serializers.CharField(
        source="stream.name",
        read_only=True,
    )

    recommendations = RecommendationSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Incident
        fields = "__all__"

        read_only_fields = [
            "created_at",
            "resolved_at",
        ]