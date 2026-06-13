from typing import TypedDict


class GraphState(TypedDict):
    cleaned_text: str

    extracted_json: dict

    valid: bool

    validation_errors: list[str]

    retry_count: int