from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()  # ✅ Loads variables from .env file

def get_llm():
    return ChatGoogleGenerativeAI(
        model="models/gemini-1.5-flash",  # ✅ fixed double 'models/models'
        convert_system_message_to_human=True,
        temperature=0.7,
        google_api_key=os.getenv("GOOGLE_API_KEY")  # ✅ safely loads from env
    )
