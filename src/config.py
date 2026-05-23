import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

DATABASE_URL = os.getenv("DATABASE_URL")

MODEL_NAME = "openai/gpt-oss-120b"
TEMPERATURE = 0.3

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in environment")

if not NEWS_API_KEY:
    raise ValueError("NEWS_API_KEY not found in environment")


if not DATABASE_URL:
    raise ValueError("DATABASE_URL not found in environment")