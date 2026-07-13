from rest_framework.routers import DefaultRouter

from .views import (
    IncidentViewSet,
    KnowledgeDocumentViewSet,
    RecommendationViewSet,
)

router = DefaultRouter()

router.register(
    "incidents",
    IncidentViewSet,
    basename="incident",
)

router.register(
    "recommendations",
    RecommendationViewSet,
    basename="recommendation",
)

router.register(
    "documents",
    KnowledgeDocumentViewSet,
    basename="document",
)

urlpatterns = router.urls