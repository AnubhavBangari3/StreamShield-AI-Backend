from langgraph.graph import END, START, StateGraph

from .nodes import (
    impact_analysis_node,
    recommendation_node,
    retrieve_runbook_node,
    root_cause_node,
    summary_node,
)
from .state import IncidentState


builder = StateGraph(IncidentState)

builder.add_node(
    "impact_analysis",
    impact_analysis_node,
)

builder.add_node(
    "retrieve_runbook",
    retrieve_runbook_node,
)

builder.add_node(
    "root_cause",
    root_cause_node,
)

builder.add_node(
    "recommendation",
    recommendation_node,
)

builder.add_node(
    "summary",
    summary_node,
)

builder.add_edge(
    START,
    "impact_analysis",
)

builder.add_edge(
    "impact_analysis",
    "retrieve_runbook",
)

builder.add_edge(
    "retrieve_runbook",
    "root_cause",
)

builder.add_edge(
    "root_cause",
    "recommendation",
)

builder.add_edge(
    "recommendation",
    "summary",
)

builder.add_edge(
    "summary",
    END,
)

workflow = builder.compile()