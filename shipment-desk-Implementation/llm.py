import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from pydantic import SecretStr

load_dotenv()

MODEL = "openai/gpt-oss-120b"

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    raise RuntimeError("GROQ_API_KEY is not set")

llm = ChatOpenAI(
    model=MODEL,
    api_key=SecretStr(api_key),
    base_url="https://api.groq.com/openai/v1",
    temperature=0,
)