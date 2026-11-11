from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import List

from dotenv import load_dotenv

# Resolve project root relative to backend/app/core
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BACKEND_DIR.parent

# Load local .env file if present
ENV_FILE = PROJECT_ROOT / ".env"
if ENV_FILE.exists():
    load_dotenv(ENV_FILE)

DEFAULT_MODEL_PATH = PROJECT_ROOT / "research" / "ISLiM" / "checkpoints" / "ISLiM_full_posestitch_pre_processed.pt"
DEFAULT_TOKENIZER_DIR = PROJECT_ROOT / "research" / "ISLiM" / "assets" / "t5-small"

# Ensure MPLCONFIGDIR is set to a writable temp path
os.environ.setdefault("MPLCONFIGDIR", os.environ.get("TEMP", "C:/Temp"))


@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = os.getenv("APP_NAME", os.getenv("PROJECT_NAME", "Signova AI Backend"))
    API_V1_STR: str = os.getenv("API_V1_PREFIX", os.getenv("API_V1_STR", "/api/v1"))
    DEBUG: bool = os.getenv("DEBUG", "false").lower() == "true"
    
    # ML Model Config
    MODEL_PATH: str = os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH))
    TOKENIZER_DIR: str = os.getenv("TOKENIZER_DIR", str(DEFAULT_TOKENIZER_DIR))
    DEVICE: str = os.getenv("MODEL_DEVICE", os.getenv("DEVICE", "cpu"))
    
    # Server & Security
    HOST: str = os.getenv("BACKEND_HOST", os.getenv("HOST", "127.0.0.1"))
    PORT: int = int(os.getenv("BACKEND_PORT", os.getenv("PORT", "8000")))
    CORS_ORIGINS: List[str] = field(
        default_factory=lambda: [
            origin.strip()
            for origin in os.getenv(
                "CORS_ORIGINS",
                f"{os.getenv('FRONTEND_URL', 'http://localhost:5173')},http://127.0.0.1:5173",
            ).split(",")
            if origin.strip()
        ]
    )


settings = Settings()
