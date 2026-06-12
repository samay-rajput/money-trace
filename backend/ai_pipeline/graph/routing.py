from backend.ai_pipeline.graph.state import StatementState


def route_after_validation(state: StatementState) -> str:
    if state.get("needs_repair"):
        return "repair"
    return "label"
