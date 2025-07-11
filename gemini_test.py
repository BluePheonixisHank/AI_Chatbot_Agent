import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv() 

genai.configure(api_key="GOOGLE_API_KEY")

model = genai.GenerativeModel("models/gemini-2.5-pro")

response = model.generate_content("Hello!")

print(response.text)
