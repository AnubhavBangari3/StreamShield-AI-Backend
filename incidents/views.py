from rest_framework import viewsets

from .models import Incident
from .serializers import IncidentSerializer


class IncidentViewSet(viewsets.ModelViewSet):
    queryset = Incident.objects.select_related("stream").all()
    serializer_class = IncidentSerializer