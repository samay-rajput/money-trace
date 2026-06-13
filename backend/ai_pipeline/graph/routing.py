from ai_pipeline.graph.state import GraphState


MAX_RETRIES = 3


def validation_router(state: GraphState) -> str:
    """
    Decides where the graph goes after validation.
    """

    if state["valid"]:
        return "success"

    if state["retry_count"] >= MAX_RETRIES:
        return "failed"

    return "repair"
