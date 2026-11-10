"""
Isolated ISL Sign Recognition Engine.
Executes sequence and video-based inference with quality validation,
optional category masking, and candidate ranking.
"""

import json
import logging
import os
from pathlib import Path
import tempfile
import time
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np
import torch
import torch.nn.functional as F

from backend.app.ml.models.temporal_cnn import TemporalCNNClassifier
from backend.app.ml.models.bilstm import BiLSTMClassifier
from backend.app.ml.preprocessing.isolated_preprocessor import (
    FEATURE_DIM,
    NUM_KEYPOINTS,
    TARGET_FRAMES,
    IsolatedSignPreprocessor,
    preprocessor,
)
from backend.app.ml.recognition.quality_validator import SignQualityValidator, quality_validator

logger = logging.getLogger("signova.ml.isolated_inference")

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
DEFAULT_CHECKPOINT_PATH = PROJECT_ROOT / "models" / "checkpoints" / "isolated_model_best.pt"
DEFAULT_LABELS_PATH = PROJECT_ROOT / "models" / "labels" / "isolated_labels.json"


class IsolatedSignRecognizer:
    """Standalone inference engine for isolated ISL gestures."""

    def __init__(
        self,
        checkpoint_path: Optional[Union[str, Path]] = None,
        labels_path: Optional[Union[str, Path]] = None,
        device: Optional[str] = None,
    ) -> None:
        self.checkpoint_path = Path(checkpoint_path or DEFAULT_CHECKPOINT_PATH)
        self.labels_path = Path(labels_path or DEFAULT_LABELS_PATH)
        
        if device:
            self.device = torch.device(device)
        else:
            self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        self.model: Optional[torch.nn.Module] = None
        self.model_type: str = "unloaded"
        self.is_loaded: bool = False
        self.labels_meta: List[Dict[str, Any]] = []
        self.idx_to_meta: Dict[int, Dict[str, Any]] = {}
        self.extractor = None

        self._load_labels()

    def _load_labels(self) -> None:
        if not self.labels_path.exists():
            raise FileNotFoundError(f"Labels file not found: {self.labels_path}")
        with open(self.labels_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.labels_meta = data["classes"]
            self.idx_to_meta = {item["index"]: item for item in self.labels_meta}

    def load_model(self) -> None:
        """Loads trained model weights into GPU/CPU memory."""
        if not self.checkpoint_path.exists():
            raise FileNotFoundError(f"Isolated model checkpoint not found: {self.checkpoint_path}")

        logger.info("Loading isolated model from %s onto %s...", self.checkpoint_path, self.device)
        checkpoint = torch.load(self.checkpoint_path, map_location=self.device, weights_only=False)

        self.model_type = checkpoint.get("model_type", "Temporal_CNN")
        in_features = checkpoint.get("in_features", 282)
        num_classes = checkpoint.get("num_classes", len(self.labels_meta))

        if self.model_type == "Temporal_CNN":
            self.model = TemporalCNNClassifier(in_features=in_features, num_classes=num_classes)
        elif self.model_type == "BiLSTM":
            self.model = BiLSTMClassifier(in_features=in_features, num_classes=num_classes)
        else:
            raise ValueError(f"Unknown model_type '{self.model_type}' in checkpoint.")

        self.model.load_state_dict(checkpoint["state_dict"])
        self.model.to(self.device)
        self.model.eval()
        self.is_loaded = True
        logger.info("Isolated model (%s) loaded successfully on %s.", self.model_type, self.device)

    def _get_extractor(self):
        """Lazy load MediaPipe Holistic extractor for video decoding."""
        if self.extractor is None:
            from research.video_pipeline.landmark_extractor import MediaPipeLandmarkExtractor
            self.extractor = MediaPipeLandmarkExtractor()
        return self.extractor

    def predict_landmarks(
        self,
        raw_keypoints: Union[np.ndarray, List[Any]],
        category: Optional[str] = None,
        top_k: int = 3,
    ) -> Dict[str, Any]:
        """
        Inference on extracted landmark sequence.
        """
        if not self.is_loaded or self.model is None:
            self.load_model()

        start_time = time.perf_counter()
        arr = np.array(raw_keypoints, dtype=np.float32)

        # Preprocess
        tensor = preprocessor.process(arr).to(self.device)  # (1, 30, 282)

        with torch.no_grad():
            logits, probs = self.model(tensor)
            try:
                probs_np = probs.cpu().numpy()[0]  # (num_classes,)
            except Exception:
                probs_np = np.array(probs.cpu().tolist()[0], dtype=np.float32)

        # Category masking if specified
        if category:
            cat_lower = category.lower().strip()
            mask = np.zeros_like(probs_np)
            for idx, meta in self.idx_to_meta.items():
                if meta["category"].lower() == cat_lower:
                    mask[idx] = 1.0
            if np.any(mask > 0):
                masked_probs = probs_np * mask
                sum_p = np.sum(masked_probs)
                if sum_p > 0:
                    probs_np = masked_probs / sum_p

        # Top candidate rankings
        top_indices = np.argsort(probs_np)[::-1][:top_k]
        top_candidates = []
        for rank_idx in top_indices:
            idx = int(rank_idx)
            meta = self.idx_to_meta.get(idx, {"label": "UNKNOWN", "display_name": "Unknown", "category": "unknown", "is_dynamic": False})
            top_candidates.append({
                "label": meta["label"],
                "display_name": meta["display_name"],
                "confidence": round(float(probs_np[idx]), 4),
                "category": meta["category"],
            })

        top_1 = top_candidates[0]
        top_meta = self.idx_to_meta.get(int(top_indices[0]), {"label": "UNKNOWN", "display_name": "Unknown", "category": "unknown", "is_dynamic": False})

        # Quality & Unknown sign validation
        val_res = quality_validator.validate(
            predicted_idx=int(top_indices[0]),
            confidence=top_1["confidence"],
            is_dynamic_sign=top_meta.get("is_dynamic", False),
            raw_keypoints=arr,
        )

        elapsed_ms = round((time.perf_counter() - start_time) * 1000.0, 2)

        return {
            "success": True,
            "predicted_sign": top_1["label"],
            "display_name": top_1["display_name"],
            "category": top_1["category"],
            "confidence": top_1["confidence"],
            "status": val_res.status,
            "is_valid": val_res.is_valid,
            "processing_time_ms": elapsed_ms,
            "model_used": self.model_type,
            "top_predictions": top_candidates,
            "reason": val_res.reason,
        }

    def predict_video(
        self,
        video_bytes: bytes,
        filename: str,
        category: Optional[str] = None,
        top_k: int = 3,
    ) -> Dict[str, Any]:
        """
        Decodes uploaded video, runs MediaPipe Holistic landmark extraction,
        and executes isolated sign classification.
        """
        suffix = Path(filename).suffix or ".mp4"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(video_bytes)
            tmp_path = Path(tmp.name)

        try:
            import cv2
            cap = cv2.VideoCapture(str(tmp_path))
            if not cap.isOpened():
                raise ValueError("Could not open video file.")

            extractor = self._get_extractor()
            frame_landmarks = []

            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                kp, _ = extractor.extract_frame(rgb_frame)  # (94, 4)
                frame_landmarks.append(kp)

            cap.release()

            if len(frame_landmarks) == 0:
                raise ValueError("No valid video frames could be decoded.")

            raw_keypoints = np.array(frame_landmarks, dtype=np.float32)  # (T, 94, 4)
            result = self.predict_landmarks(raw_keypoints, category=category, top_k=top_k)
            return result
        finally:
            if tmp_path.exists():
                try:
                    tmp_path.unlink()
                except Exception:
                    pass
