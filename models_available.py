import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()

genai.configure(api_key="GOOGLE_API_KEY")

models = genai.list_models()

for model in models:
    print(model.name)
