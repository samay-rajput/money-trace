from typing import Any


def validate_transactions(transactions: list[dict[str, Any]]) -> dict[str, Any]:
    errors = []

    if not isinstance(transactions, list):
        errors.append("Transactions must be a list.")

    return {
        "is_valid": not errors,
        "errors": errors,
    }
