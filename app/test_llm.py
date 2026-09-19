import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not configured in .env")


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash",
    google_api_key=api_key,
)

response = model.invoke(
    "You are FinSource, a financial education assistant. "
    "Reply with exactly: FinSource AI is connected successfully."
)

print(response.text)