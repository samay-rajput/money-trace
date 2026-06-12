from backend.ai_pipeline.agents.labeling_agent import label_expenses
from backend.ai_pipeline.agents.repair_agent import repair_transactions
from backend.ai_pipeline.agents.structuring_agent import build_table
from backend.ai_pipeline.agents.validation_agent import validate_transactions
from backend.ai_pipeline.graph.routing import route_after_validation
from backend.ai_pipeline.graph.state import StatementState


def structure_node(state: StatementState) -> StatementState:
    state["transactions"] = build_table(state.get("cleaned_text", ""))
    return state


def validation_node(state: StatementState) -> StatementState:
    validation_result = validate_transactions(state.get("transactions", []))
    state["validation_errors"] = validation_result["errors"]
    state["needs_repair"] = not validation_result["is_valid"]
    return state


def repair_node(state: StatementState) -> StatementState:
    state["transactions"] = repair_transactions(
        state.get("transactions", []),
        state.get("validation_errors", []),
    )
    state["needs_repair"] = False
    return state


def labeling_node(state: StatementState) -> StatementState:
    state["labeled_transactions"] = label_expenses(state.get("transactions", []))
    return state


def run_statement_workflow(state: StatementState) -> StatementState:
    state = structure_node(state)
    state = validation_node(state)
    if route_after_validation(state) == "repair":
        state = repair_node(state)
    return labeling_node(state)
