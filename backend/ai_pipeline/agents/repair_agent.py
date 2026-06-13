from ai_pipeline.graph.state import GraphState

from ai_pipeline.schemas.statement_schema import Statement

from ai_pipeline.llm.llm_router import generate_structured


# Instructions for repairing invalid extraction output
REPAIR_PROMPT = """
You are a bank statement extraction repair agent.

You are given:

1. Original OCR text
2. Previously extracted JSON
3. Validation errors

Your task:

- Fix only the reported issues.
- Preserve correct transactions.
- Do not invent transactions.
- Do not remove valid transactions.
- Return data matching the provided schema.
"""


def repair_agent(state: GraphState) -> GraphState:
    """
    Agent-3

    Input:
        OCR text
        Invalid extracted JSON
        Validation errors

    Output:
        Repaired JSON
    """

    cleaned_text = state["cleaned_text"]

    extracted_json = state["extracted_json"]

    validation_errors = state["validation_errors"]

    prompt = f"""
{REPAIR_PROMPT}

OCR TEXT:
{cleaned_text}

CURRENT JSON:
{extracted_json}

VALIDATION ERRORS:
{validation_errors}
"""

    # Ask LLM to repair the invalid extraction
    repaired_result: Statement = generate_structured(
        prompt=prompt,
        schema=Statement
    )

    # Update graph state with repaired output
    state["extracted_json"] = repaired_result.model_dump()

    # Track repair attempts
    state["retry_count"] += 1

    return state
