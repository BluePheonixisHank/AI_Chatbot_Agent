# agent.py
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()  # Loads variables from .env file

def get_llm():
    """Returns a configured instance of the Gemini LLM."""
    return ChatGoogleGenerativeAI(
        model="gemini-1.5-pro",
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )