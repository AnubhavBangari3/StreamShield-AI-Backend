from typing import TypedDict


class IncidentState(TypedDict):
    incident_id: int

    incident_title: str
    incident_type: str
    severity: str
    region: str
    affected_users: int

    runbooks: list[str]

    root_cause: str
    recommendations: list[str]
    summary: str

    confidence: float