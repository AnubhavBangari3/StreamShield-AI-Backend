from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    StreamMetricViewSet,
    StreamViewSet,
    dashboard_summary,
)

router = DefaultRouter()
router.register("streams", StreamViewSet, basename="stream")
router.register("metrics", StreamMetricViewSet, basename="metric")

urlpatterns = [
    path(
        "dashboard/",
        dashboard_summary,
        name="dashboard-summary",
    ),
]

urlpatterns += router.urls