from dotenv import load_dotenv
import os

from langchain_groq import ChatGroq


load_dotenv()

if os.getenv("GROQ_API_KEY") is None:
    raise ValueError("GROQ_API_KEY environment variable is not set.")
else:
    print("GROQ_API_KEY is set.")


llm_groq = ChatGroq(
    model="openai/gpt-oss-120b",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.7
)