import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

gemini_api_key = os.getenv("GEMINI_API_KEY")


llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", api_key=gemini_api_key)
