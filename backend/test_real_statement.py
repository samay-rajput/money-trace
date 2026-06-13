import json
from pathlib import Path

from ai_pipeline.ocr.extract_text import extract_text_auto
from ai_pipeline.preprocessing.text_cleaning import clean_text

from ai_pipeline.graph.workflow import workflow
from ai_pipeline.config import load_environment
import os

load_environment()

print("Gemini loaded:", bool(os.getenv("GEMINI_API_KEY")))
print("Groq loaded:", bool(os.getenv("GROQ_API_KEY")))
PDF_PATH = Path(__file__).resolve().parent.parent / "sample_pdfs" / "sample_statement.pdf"


def main():

    print("=" * 60)
    print("STEP 1 : OCR")
    print("=" * 60)

    raw_text = extract_text_auto(PDF_PATH)

    print(raw_text[:1000])

    print("\n" + "=" * 60)
    print("STEP 2 : CLEANING")
    print("=" * 60)

    cleaned_text = clean_text(raw_text)

    print(cleaned_text[:1000])

    print("\n" + "=" * 60)
    print("STEP 3 : GRAPH EXECUTION")
    print("=" * 60)

    initial_state = {
        "cleaned_text": cleaned_text,
        "extracted_json": {},
        "valid": False,
        "validation_errors": [],
        "retry_count": 0,
    }

    result = workflow.invoke(initial_state)

    print("\n" + "=" * 60)
    print("FINAL EXTRACTED JSON")
    print("=" * 60)

    print(
        json.dumps(
            result["extracted_json"],
            indent=4
        )
    )

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)

    print(f"Valid: {result['valid']}")
    print(f"Repair Attempts: {result['retry_count']}")

    if result["validation_errors"]:
        print("\nValidation Errors:")

        for err in result["validation_errors"]:
            print(f"- {err}")


if __name__ == "__main__":
    main()
