from rest_framework.routers import DefaultRouter

from .views import StreamMetricViewSet, StreamViewSet

router = DefaultRouter()
router.register("streams", StreamViewSet)
router.register("metrics", StreamMetricViewSet)

urlpatterns = router.urls