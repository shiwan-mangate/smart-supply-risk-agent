import os
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = "llama-3.3-70b-versatile"
TEMPERATURE = 0.3

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY not found in .env")