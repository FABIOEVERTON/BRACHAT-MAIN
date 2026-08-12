import os

from dotenv import load_dotenv

load_dotenv()


def get_int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


def get_float(name: str, default: float) -> float:
    try:
        return float(os.getenv(name, default))
    except (TypeError, ValueError):
        return default


LLM_PROVIDER = os.getenv("LLM_PROVIDER", "google")
LLM_MODEL = os.getenv("LLM_MODEL", "gemini-2.5-flash")
EMBEDDING_PROVIDER = os.getenv("EMBEDDING_PROVIDER", "google")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-001")
EMBEDDING_FALLBACK = os.getenv("EMBEDDING_FALLBACK", "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")

VECTOR_DB_DIR = os.getenv("VECTOR_DB_DIR", "./chroma")
DATA_DIR = os.getenv("DATA_DIR", "./data")
LOG_DIR = os.getenv("LOG_DIR", "./logs")

CONFIDENCE_THRESHOLD = get_float("CONFIDENCE_THRESHOLD", 0.45)
TOP_K = get_int("TOP_K", 5)
RERANK_TOP_K = get_int("RERANK_TOP_K", 3)

DATA_INCLUDE = [s.strip() for s in os.getenv("DATA_INCLUDE", "").split(",") if s.strip()]

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
OMNIRoute_API_KEY = os.getenv("OMNIRoute_API_KEY", "")
