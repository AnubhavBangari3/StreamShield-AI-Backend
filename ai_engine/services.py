from incidents.models import Incident

from .graph import workflow


def analyze_incident(incident_id: int):
    incident = Incident.objects.get(id=incident_id)

    state = {
        "incident_id": incident.id,
        "incident_title": incident.title,
        "incident_type": incident.incident_type,
        "severity": incident.severity,
        "region": incident.region,
        "affected_users": incident.affected_users,
        "runbooks": [],
        "root_cause": "",
        "recommendations": [],
        "summary": "",
        "confidence": 0.0,
    }

    result = workflow.invoke(state)

    return result