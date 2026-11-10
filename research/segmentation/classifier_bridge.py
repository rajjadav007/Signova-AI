"""
Classifier bridge connecting segment landmarks to the existing ISLiM model (Phase 4).
Loads ISLiM once and evaluates individual segments as well as full video baseline.
"""

from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Optional, Union
import numpy as np

# Ensure research paths in sys.path
SEG_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SEG_DIR.parent.parent
ISLIM_DIR = PROJECT_ROOT / "research" / "ISLiM"
for p in [str(PROJECT_ROOT), str(ISLIM_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

try:
    from research.ISLiM.inference.predictor import ISLiMPredictor
except ImportError:
    from inference.predictor import ISLiMPredictor  # type: ignore[import-not-found]

try:
    from backend.app.ml.recognition.isolated_inference import IsolatedSignRecognizer
except ImportError:
    IsolatedSignRecognizer = None


class SegmentClassifierBridge:
    """
    Executes sign recognition inference on segmented landmark sequences
    using both Phase 3 Isolated Sign Classifier and Phase 2 ISLiM model.
    """

    def __init__(
        self,
        checkpoint_path: Optional[Union[str, Path]] = None,
        tokenizer_dir: Optional[Union[str, Path]] = None,
        isolated_checkpoint_path: Optional[Union[str, Path]] = None,
        device: str = "auto",
    ):
        ckpt = Path(
            checkpoint_path
            or ISLIM_DIR / "checkpoints" / "ISLiM_full_posestitch_pre_processed.pt"
        ).resolve()
        tok = Path(tokenizer_dir or ISLIM_DIR / "assets" / "t5-small").resolve()

        if not ckpt.exists():
            raise FileNotFoundError(f"ISLiM checkpoint not found at: {ckpt}")

        self.predictor = ISLiMPredictor(
            checkpoint_path=str(ckpt),
            tokenizer_dir=str(tok),
            device=device,
        )
        self.device = self.predictor.device

        # Initialize Phase 3 Isolated Sign Recognizer if available
        self.isolated_recognizer: Optional[Any] = None
        iso_ckpt = Path(
            isolated_checkpoint_path
            or PROJECT_ROOT / "models" / "checkpoints" / "isolated_model_best.pt"
        ).resolve()
        if IsolatedSignRecognizer is not None and iso_ckpt.exists():
            try:
                self.isolated_recognizer = IsolatedSignRecognizer(checkpoint_path=str(iso_ckpt))
                self.isolated_recognizer.load_model()
            except Exception:
                self.isolated_recognizer = None

    def classify_segment(
        self,
        segment_landmarks: np.ndarray,
        is_valid: bool = True,
        decoding: str = "beam",
    ) -> Dict[str, Any]:
        """
        Run isolated gesture translation on a single segment.

        Args:
            segment_landmarks: (T_seg, 94, 4) float32 landmark array
            is_valid: Whether segment passed validation criteria
            decoding: 'beam' or 'greedy'

        Returns:
            Dictionary with prediction text, tokens, inference timing, and rejection flag.
        """
        if not is_valid:
            return {
                "prediction": "[REJECTED_SEGMENT]",
                "token_ids": [],
                "inference_time_ms": 0.0,
                "is_rejected": True,
                "rejection_reason": "Failed segment validation",
            }

        t_start = time.perf_counter()
        isolated_meta = None
        if self.isolated_recognizer is not None and getattr(self.isolated_recognizer, "is_loaded", False):
            try:
                iso_res = self.isolated_recognizer.predict_landmarks(segment_landmarks, top_k=3)
                isolated_meta = {
                    "predicted_sign": iso_res.get("predicted_sign"),
                    "display_name": iso_res.get("display_name"),
                    "confidence": iso_res.get("confidence"),
                    "is_valid": iso_res.get("is_valid"),
                    "status": iso_res.get("status"),
                    "top_candidates": iso_res.get("top_predictions", []),
                }
            except Exception as exc:
                isolated_meta = {"error": str(exc)}

        try:
            res = self.predictor.predict(
                keypoints=segment_landmarks,
                decoding=decoding,
            )
            elapsed_ms = (time.perf_counter() - t_start) * 1000.0

            pred_text = res.get("prediction", "").strip()
            tokens = res.get("token_ids", [])

            # Unknown sign rejection: empty string, or token only <unk>
            is_unknown = (
                len(pred_text) == 0
                or pred_text.lower() in ("unknown", "<unk>", "")
            )

            out_dict = {
                "prediction": pred_text if not is_unknown else "[UNKNOWN_SIGN]",
                "token_ids": tokens,
                "inference_time_ms": round(elapsed_ms, 2),
                "is_rejected": is_unknown,
                "rejection_reason": "Confidence below threshold / unknown token" if is_unknown else None,
            }
            if isolated_meta is not None:
                out_dict["phase3_isolated_prediction"] = isolated_meta
            return out_dict
        except Exception as e:
            elapsed_ms = (time.perf_counter() - t_start) * 1000.0
            return {
                "prediction": "[INFERENCE_ERROR]",
                "token_ids": [],
                "inference_time_ms": round(elapsed_ms, 2),
                "is_rejected": True,
                "rejection_reason": str(e),
            }

    def classify_full_video(
        self,
        full_keypoints: np.ndarray,
        decoding: str = "beam",
    ) -> Dict[str, Any]:
        """
        Run baseline full-video ISLiM sentence translation without segmentation.
        """
        t_start = time.perf_counter()
        res = self.predictor.predict(
            keypoints=full_keypoints,
            decoding=decoding,
        )
        elapsed_ms = (time.perf_counter() - t_start) * 1000.0

        return {
            "prediction": res.get("prediction", "").strip(),
            "token_ids": res.get("token_ids", []),
            "inference_time_ms": round(elapsed_ms, 2),
        }
