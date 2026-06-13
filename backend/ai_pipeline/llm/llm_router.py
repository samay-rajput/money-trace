from typing import Type

from pydantic import BaseModel

from ai_pipeline.llm.gemini_client import get_gemini_llm
from ai_pipeline.llm.groq_client import get_groq_llm


def generate(prompt: str) -> str:

    try:
        llm = get_gemini_llm()

        response = llm.invoke(prompt)

        return response.content

    except Exception:

        llm = get_groq_llm()

        response = llm.invoke(prompt)

        return response.content


def generate_structured(
    prompt: str,
    schema: Type[BaseModel]
):

    # try:

    #     llm = get_gemini_llm()

    #     structured_llm = llm.with_structured_output(schema)

    #     return structured_llm.invoke(prompt)

    # except Exception:

    #     llm = get_groq_llm()

    #     structured_llm = llm.with_structured_output(schema)

    #     return structured_llm.invoke(prompt)
    try:

        print("Using Gemini")

        llm = get_gemini_llm()

        structured_llm = llm.with_structured_output(schema)

        result = structured_llm.invoke(prompt)

        print("Gemini Success")

        return result

    except Exception as e:

        print("\nGemini Failed")
        print(type(e).__name__)
        print(e)

        raise
