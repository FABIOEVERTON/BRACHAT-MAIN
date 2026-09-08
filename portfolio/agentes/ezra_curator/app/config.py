import os
from pathlib import Path

from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()


# ============================================================
# HELPERS
# ============================================================

def get_int(name: str, default: int) -> int:
    """Read an integer environment variable safely."""
    try:
        return int(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


def get_float(name: str, default: float) -> float:
    """Read a float environment variable safely."""
    try:
        return float(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        return default


def get_str(name: str, default: str = "") -> str:
    """Read a string environment variable safely."""
    return os.getenv(name, default).strip()


# ============================================================
# LLM CONFIGURATION
# ============================================================

LLM_PROVIDER = get_str("LLM_PROVIDER", "google")
LLM_MODEL = get_str("LLM_MODEL", "gemini-2.5-flash")


# ============================================================
# EMBEDDING CONFIGURATION
# ============================================================

EMBEDDING_PROVIDER = get_str("EMBEDDING_PROVIDER", "google")

EMBEDDING_MODEL = get_str(
    "EMBEDDING_MODEL",
    "models/gemini-embedding-001",
)

EMBEDDING_FALLBACK = get_str(
    "EMBEDDING_FALLBACK",
    "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
)


# ============================================================
# DIRECTORIES
# ============================================================

VECTOR_DB_DIR = Path(
    get_str("VECTOR_DB_DIR", "./chroma")
)

DATA_DIR = Path(
    get_str("DATA_DIR", "./data")
)

LOG_DIR = Path(
    get_str("LOG_DIR", "./logs")
)


# ============================================================
# RAG PARAMETERS
# ============================================================

CONFIDENCE_THRESHOLD = get_float(
    "CONFIDENCE_THRESHOLD",
    0.45,
)

TOP_K = get_int(
    "TOP_K",
    5,
)

RERANK_TOP_K = get_int(
    "RERANK_TOP_K",
    3,
)


# ============================================================
# DATA FILTERING
# ============================================================

DATA_INCLUDE = [
    item.strip()
    for item in get_str("DATA_INCLUDE", "").split(",")
    if item.strip()
]


# ============================================================
# API KEYS
# ============================================================

GOOGLE_API_KEY = get_str("GOOGLE_API_KEY")
GROQ_API_KEY = get_str("GROQ_API_KEY")
ANTHROPIC_API_KEY = get_str("ANTHROPIC_API_KEY")
COHERE_API_KEY = get_str("COHERE_API_KEY")
MISTRAL_API_KEY = get_str("MISTRAL_API_KEY")

# Keep the environment variable name exactly as defined in .env
OMNIROUTE_API_KEY = get_str("OMNIRoute_API_KEY")