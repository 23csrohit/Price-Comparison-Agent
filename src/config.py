import os
from dotenv import load_dotenv
from crewai import LLM

load_dotenv()

# Load API keys from environment variables
CEREBRAS_API_KEY = os.getenv("CEREBRAS_API_KEY")
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

if not CEREBRAS_API_KEY:
    raise ValueError("Missing Cerebras API Key! Set CEREBRAS_API_KEY in environment variables.")

if not SERPER_API_KEY:
    raise ValueError("Missing Serper API Key! Set SERPER_API_KEY in environment variables.")

cerebras_llm = LLM(
    model="cerebras/llama-3.3-70b",
    temperature=0.7,
    max_tokens=18192,
    api_key=CEREBRAS_API_KEY,
    base_url="https://api.cerebras.ai/v1",
)