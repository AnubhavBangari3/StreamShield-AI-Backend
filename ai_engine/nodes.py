from knowledge_base.retriever import retrieve_documents


def impact_analysis_node(state):
    return state


def retrieve_runbook_node(state):
    query = (
        f"{state['incident_type']} "
        f"{state['severity']} "
        f"{state['region']}"
    )

    docs = retrieve_documents(query)

    state["runbooks"] = [
        doc.page_content
        for doc in docs
    ]

    return state


def root_cause_node(state):
    state["root_cause"] = (
        "Placeholder root cause generated from retrieved runbooks."
    )

    return state


def recommendation_node(state):
    state["recommendations"] = [
        "Inspect CDN health.",
        "Route traffic to another region.",
        "Reduce bitrate temporarily.",
    ]

    return state


def summary_node(state):
    state["summary"] = (
        f"{state['severity'].title()} incident affecting "
        f"{state['affected_users']} users."
    )

    state["confidence"] = 0.82

    return state