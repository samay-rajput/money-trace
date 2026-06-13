import os

from langchain_google_genai import ChatGoogleGenerativeAI

from ai_pipeline.config import load_environment


load_environment()


def get_gemini_llm():

    return ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )


