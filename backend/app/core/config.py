from dataclasses import dataclass, field
import os
from pathlib import Path
from typing import List

# Resolve project root relative to backend/app/core
BACKEND_DIR = Path(__file__).resolve().parent.parent.parent
PROJECT_ROOT = BACKEND_DIR.parent
DEFAULT_MODEL_PATH = PROJECT_ROOT / "research" / "ISLiM" / "checkpoints" / "ISLiM_full_posestitch_pre_processed.pt"
DEFAULT_TOKENIZER_DIR = PROJECT_ROOT / "research" / "ISLiM" / "assets" / "t5-small"

# Ensure MPLCONFIGDIR is set to a writable temp path
os.environ["MPLCONFIGDIR"] = os.environ.get("TEMP", "C:/Temp")


@dataclass(frozen=True)
class Settings:
    PROJECT_NAME: str = "Signova AI Backend"
    API_V1_STR: str = "/api/v1"
    
    # ML Model Config
    MODEL_PATH: str = os.getenv("MODEL_PATH", str(DEFAULT_MODEL_PATH))
    TOKENIZER_DIR: str = os.getenv("TOKENIZER_DIR", str(DEFAULT_TOKENIZER_DIR))
    DEVICE: str = os.getenv("DEVICE", "auto")
    
    # Server & Security
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: List[str] = field(
        default_factory=lambda: [
            origin.strip() for origin in os.getenv("CORS_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173,*").split(",") if origin.strip()
        ]
    )


settings = Settings()
