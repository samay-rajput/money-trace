import os

from langchain_groq import ChatGroq

from ai_pipeline.config import load_environment


load_environment()


def get_groq_llm():

    return ChatGroq(
        model="llama-3.3-70b-versatile",
        groq_api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )
