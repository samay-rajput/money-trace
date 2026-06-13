import os

from ai_pipeline.config import load_environment


load_environment()

print("Gemini loaded:", bool(os.getenv("GEMINI_API_KEY")))
print("Groq loaded:", bool(os.getenv("GROQ_API_KEY")))
