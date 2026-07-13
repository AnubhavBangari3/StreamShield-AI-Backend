from django.utils import timezone
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Incident,
    KnowledgeDocument,
    Recommendation,
)
from .serializers import (
    IncidentSerializer,
    KnowledgeDocumentSerializer,
    RecommendationSerializer,
)


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.select_related("stream").prefetch_related(
        "recommendations"
    )
    serializer_class = IncidentSerializer

    @action(detail=True, methods=["patch"])
    def resolve(self, request, pk=None):
        incident = self.get_object()

        incident.status = "resolved"
        incident.resolved_at = timezone.now()

        incident.save(
            update_fields=[
                "status",
                "resolved_at",
            ]
        )

        return Response(
            self.get_serializer(incident).data
        )


class RecommendationViewSet(viewsets.ModelViewSet):
    queryset = Recommendation.objects.select_related(
        "incident"
    ).all()

    serializer_class = RecommendationSerializer

    @action(detail=True, methods=["patch"])
    def complete(self, request, pk=None):
        recommendation = self.get_object()

        recommendation.is_completed = True
        recommendation.save(update_fields=["is_completed"])

        return Response(
            self.get_serializer(recommendation).data
        )


class KnowledgeDocumentViewSet(viewsets.ModelViewSet):
    queryset = KnowledgeDocument.objects.all()
    serializer_class = KnowledgeDocumentSerializer