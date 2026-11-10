import logging
import os
from pathlib import Path
import sys
import tempfile
from typing import Any, Dict, Optional

from backend.app.core.config import settings

logger = logging.getLogger("signova.inference")

# Ensure research paths are in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
ISLIM_DIR = PROJECT_ROOT / "research" / "ISLiM"
RESEARCH_DIR = PROJECT_ROOT / "research"

for p in [str(PROJECT_ROOT), str(RESEARCH_DIR), str(ISLIM_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)


class InferenceService:
    """Service wrapping ISLiM video translation pipeline."""

    def __init__(self) -> None:
        self.pipeline: Optional[Any] = None
        self.is_loaded: bool = False
        self.device_info: str = "uninitialized"

    def load_model(self) -> None:
        """Instantiate VideoToISLiMPipeline once at application startup."""
        if self.is_loaded and self.pipeline is not None:
            logger.info("ISLiM pipeline already loaded in memory.")
            return

        checkpoint = Path(settings.MODEL_PATH).resolve()
        tokenizer_dir = Path(settings.TOKENIZER_DIR).resolve()

        if not checkpoint.exists():
            raise FileNotFoundError(
                f"ISLiM checkpoint not found at: {checkpoint}. Verify MODEL_PATH."
            )

        logger.info("Initializing VideoToISLiMPipeline with checkpoint: %s", checkpoint)
        from research.video_pipeline.video_inference_pipeline import VideoToISLiMPipeline

        self.pipeline = VideoToISLiMPipeline(
            checkpoint_path=str(checkpoint),
            tokenizer_dir=str(tokenizer_dir),
            device=settings.DEVICE,
        )
        self.is_loaded = True
        self.device_info = str(self.pipeline.device)
        logger.info("ISLiM pipeline loaded successfully on device: %s", self.device_info)

    def predict_video_file(
        self,
        video_bytes: bytes,
        filename: str,
        decoding: str = "beam",
    ) -> Dict[str, Any]:
        """
        Process video bytes through temporary file and invoke ISLiM inference.
        """
        if not self.is_loaded or self.pipeline is None:
            raise RuntimeError("Model pipeline is not loaded.")

        # Preserve file extension
        suffix = Path(filename).suffix or ".mp4"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(video_bytes)
            tmp_path = Path(tmp.name)

        try:
            result = self.pipeline.predict_video(
                video_path=tmp_path,
                decoding=decoding,
                save_output=False,
            )
            return result
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except Exception as exc:
                    logger.warning("Failed to remove temporary video file %s: %s", tmp_path, exc)


# Global service instance
inference_service = InferenceService()
