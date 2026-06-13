
from schemas.statement_schema import Statement
from graph.state import GraphState

from pydantic import ValidationError

"""
    Validates extracted transaction JSON.

    Updates:
        state["valid"]
        state["validation_errors"]
"""

def validation_agent(state: GraphState) -> GraphState:

    extracted_json = state["extracted_json"]

    errors = []

    try:
        Statement.model_validate(extracted_json)

    except ValidationError as e:
        errors.extend(
            [err["msg"] for err in e.errors()]
        )

    state["valid"] = len(errors) == 0
    state["validation_errors"] = errors

    return state