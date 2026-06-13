from datetime import datetime

from pydantic import ValidationError

from ai_pipeline.graph.state import GraphState
from ai_pipeline.schemas.statement_schema import Statement


def validation_agent(state: GraphState) -> GraphState:
    """
    Agent-2

    Validates extracted transaction JSON.

    Checks:
    - Pydantic schema
    - Date format
    - Transaction count
    - Amount validity
    """

    extracted_json = state["extracted_json"]

    errors = []

    # -------------------------
    # Schema Validation
    # -------------------------

    try:
        statement = Statement.model_validate(extracted_json)

    except ValidationError as e:

        errors.extend(
            [err["msg"] for err in e.errors()]
        )

        state["valid"] = False
        state["validation_errors"] = errors

        return state

    # -------------------------
    # Business Validation
    # -------------------------

    if len(statement.accounts) == 0:
        errors.append("No accounts found")

    for account in statement.accounts:

        if len(account.transactions) == 0:
            errors.append(
                "Account contains no transactions"
            )

        for txn in account.transactions:

            # Amount must be positive
            if txn.amount <= 0:
                errors.append(
                    f"Invalid amount: {txn.amount}"
                )

            # Validate date format
            try:
                datetime.strptime(
                    txn.date,
                    "%Y-%m-%d"
                )

            except ValueError:

                errors.append(
                    f"Invalid date format: {txn.date}"
                )

    state["valid"] = len(errors) == 0
    state["validation_errors"] = errors

    return state