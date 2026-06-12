from typing import Any, TypedDict


class StatementState(TypedDict, total=False):
    file_path: str
    raw_text: str
    cleaned_text: str
    transactions: list[dict[str, Any]]
    labeled_transactions: list[dict[str, Any]]
    validation_errors: list[str]
    needs_repair: bool
