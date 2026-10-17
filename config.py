"""
config.py – Central configuration for the Customer Support Triage Crew.
All env vars and system-level settings are loaded here.
"""

import os
from dotenv import load_dotenv

load_dotenv()

# ─── LLM Settings (Google Gemini) ───────────────────────────────────────────
GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
PRIMARY_MODEL: str = os.getenv("PRIMARY_MODEL", "gemini-3.6-flash")
CHEAP_MODEL: str = os.getenv("CHEAP_MODEL", "gemini-3.6-flash")

# Push so google-generativeai SDK picks it up automatically
os.environ["GOOGLE_API_KEY"] = GOOGLE_API_KEY

# ─── LangSmith ──────────────────────────────────────────────────────────────
LANGCHAIN_API_KEY: str = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_PROJECT: str = os.getenv("LANGCHAIN_PROJECT", "customer-support-triage")
LANGCHAIN_TRACING_V2: str = os.getenv("LANGCHAIN_TRACING_V2", "true")
LANGCHAIN_ENDPOINT: str = os.getenv(
    "LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com"
)

# Push env vars so LangSmith SDK picks them up automatically
os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
os.environ["LANGCHAIN_TRACING_V2"] = LANGCHAIN_TRACING_V2
os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT

# ─── Vector Store ───────────────────────────────────────────────────────────
CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", "./chroma_db")
COLLECTION_NAME: str = "support_kb"
TOP_K_RESULTS: int = 4

# ─── Crew Logic ─────────────────────────────────────────────────────────────
CONFIDENCE_THRESHOLD: float = float(os.getenv("CONFIDENCE_THRESHOLD", "0.7"))
MAX_REVISION_LOOPS: int = int(os.getenv("MAX_REVISION_LOOPS", "1"))

# ─── Categories & Priorities ────────────────────────────────────────────────
VALID_CATEGORIES = ["billing", "technical", "account", "general"]
VALID_PRIORITIES = ["low", "medium", "high"]

# ─── LangSmith Dataset ──────────────────────────────────────────────────────
DATASET_NAME: str = "support-triage-eval-v1"

# ─── Gemini Embedding Model ─────────────────────────────────────────────────
EMBEDDING_MODEL: str = "models/gemini-embedding-2"
