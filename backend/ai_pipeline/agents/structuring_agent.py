from ai_pipeline.graph.state import GraphState

from ai_pipeline.schemas.statement_schema import Statement

from ai_pipeline.llm.llm_router import generate_structured


# Instructions given to the LLM for transaction extraction
SYSTEM_PROMPT = """
You are an expert bank statement parser.

Your task is to convert OCR extracted bank statement text
into structured transaction data.

Rules:

1. Work across any bank.
2. Detect transaction boundaries.
3. Merge multiline descriptions.
4. Extract:
   - date
   - description
   - amount
   - type (debit/credit)
   - balance
5. Detect multiple account sections.
6. If account number is unknown, use null.
7. Ignore headers, footers, summaries and page numbers.
8. Return only data that fits the provided schema.
"""


def structuring_agent(state: GraphState) -> GraphState:
    """
    Agent-1

    Input:
        OCR cleaned text

    Output:
        Structured transaction JSON
    """

    cleaned_text = state["cleaned_text"]

    # Build the final prompt sent to Gemini/Groq
    prompt = f"""
        {SYSTEM_PROMPT}

        OCR TEXT:

        {cleaned_text}
        """

    # Ask the LLM to directly populate our Statement schema
    result: Statement = generate_structured(
        prompt=prompt,
        schema=Statement
    )

    # Convert Pydantic object into dictionary
    # so the next graph node can consume it
    state["extracted_json"] = result.model_dump()

    return state
