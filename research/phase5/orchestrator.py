"""
Signova AI - Python-Only Integration Orchestrator (Phase 5).
Connects and evaluates:
  - Mode A: Isolated / Segmented Sign Recognition (MediaPipe -> Phase 4 Segmentation -> Phase 3 Temporal CNN)
  - Mode B: Continuous Sentence Translation (Full Video -> Official ISLiM Preprocessing -> ISLiM Checkpoint)
With strict decoupling, confidence validation, timestamp preservation, and asynchronous TTS.
"""

from collections import Counter
import logging
from pathlib import Path
import re
import sys
import time
from typing import Any, Dict, List, Optional, Tuple, Union
import numpy as np

# Ensure research and project root paths in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ISLIM_DIR = PROJECT_ROOT / "research" / "ISLiM"
RESEARCH_DIR = PROJECT_ROOT / "research"
BACKEND_DIR = PROJECT_ROOT / "backend"

for p in [str(PROJECT_ROOT), str(RESEARCH_DIR), str(ISLIM_DIR), str(BACKEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from research.phase5.tts_module import SignovaTTS
from research.segmentation.boundary_detector import ContinuousSignSegmenter
from research.segmentation.config import SegmentationConfig
from research.segmentation.segment_extractor import SegmentExtractor
from backend.app.ml.recognition.isolated_inference import IsolatedSignRecognizer
from backend.app.ml.recognition.quality_validator import SignQualityValidator, quality_validator

try:
    from research.ISLiM.inference.predictor import ISLiMPredictor
except ImportError:
    from inference.predictor import ISLiMPredictor  # type: ignore[import-not-found]

logger = logging.getLogger("signova.phase5.orchestrator")


class SignovaOrchestrator:
    """
    Central Python Integration Orchestrator for Signova AI Phase 5.
    Provides selectable Mode A (Segmented) and Mode B (Continuous ISLiM) pipelines.
    """

    def __init__(
        self,
        device: str = "auto",
        enable_tts: bool = False,
        tts_debounce: float = 2.0,
        segmentation_approach: str = "combined",
        islim_checkpoint: Optional[Union[str, Path]] = None,
        isolated_checkpoint: Optional[Union[str, Path]] = None,
    ) -> None:
        self.device = device
        self.enable_tts = enable_tts
        self.segmentation_approach = segmentation_approach

        # 1. Initialize Phase 4 Segmenter & Extractor
        self.seg_config = SegmentationConfig(approach=segmentation_approach)
        self.segmenter = ContinuousSignSegmenter(self.seg_config)
        self.extractor = SegmentExtractor(self.seg_config)

        # 2. Lazy / Explicit Loaders for Models
        self._islim_checkpoint_path = Path(
            islim_checkpoint
            or ISLIM_DIR / "checkpoints" / "ISLiM_full_posestitch_pre_processed.pt"
        ).resolve()
        self._isolated_checkpoint_path = Path(
            isolated_checkpoint
            or PROJECT_ROOT / "models" / "checkpoints" / "isolated_model_best.pt"
        ).resolve()

        self._islim_predictor: Optional[ISLiMPredictor] = None
        self._isolated_recognizer: Optional[IsolatedSignRecognizer] = None
        self.quality_validator: SignQualityValidator = quality_validator

        # 3. Text-to-Speech Engine
        self.tts = SignovaTTS(enabled=enable_tts, debounce_seconds=tts_debounce)

    # -------------------------------------------------------------------------
    # Model Accessors
    # -------------------------------------------------------------------------
    @property
    def islim_predictor(self) -> ISLiMPredictor:
        if self._islim_predictor is None:
            logger.info("Loading ISLiM model from %s...", self._islim_checkpoint_path)
            tok_dir = ISLIM_DIR / "assets" / "t5-small"
            self._islim_predictor = ISLiMPredictor(
                checkpoint_path=str(self._islim_checkpoint_path),
                tokenizer_dir=str(tok_dir),
                device=self.device,
            )
        return self._islim_predictor

    @property
    def isolated_recognizer(self) -> IsolatedSignRecognizer:
        if self._isolated_recognizer is None:
            logger.info("Loading Isolated Recognizer from %s...", self._isolated_checkpoint_path)
            self._isolated_recognizer = IsolatedSignRecognizer(
                checkpoint_path=str(self._isolated_checkpoint_path),
                device=self.device if self.device != "auto" else None,
            )
            self._isolated_recognizer.load_model()
        return self._isolated_recognizer

    # -------------------------------------------------------------------------
    # Mode A: Isolated / Segmented Recognition
    # Video -> MediaPipe landmarks -> Phase 4 segmentation -> Phase 3 Temporal CNN
    # -------------------------------------------------------------------------
    def run_mode_a(
        self,
        keypoints: np.ndarray,
        fps: float = 30.0,
        category_filter: Optional[str] = None,
        top_k: int = 3,
    ) -> Dict[str, Any]:
        """
        Executes Mode A: Segmented Isolated Sign Recognition.
        Each detected segment is independently extracted, validated, and classified.
        Preserves original start/end timestamps and top-k candidates.
        """
        t0 = time.perf_counter()
        if len(keypoints) == 0:
            return {
                "mode": "Mode_A_Isolated_Segmented",
                "success": False,
                "error": "Empty keypoints input.",
                "segments": [],
                "latency_ms": 0.0,
            }

        # 1. Perform Boundary Detection
        t_seg_start = time.perf_counter()
        seg_res = self.segmenter.segment(keypoints, fps=fps, approach=self.segmentation_approach)
        raw_boundaries = seg_res["raw_segments"]
        features = seg_res["features"]
        seg_latency_ms = (time.perf_counter() - t_seg_start) * 1000.0

        # 2. Extract and Validate Segments
        extracted_segments = self.extractor.extract_segments(
            keypoints,
            raw_boundaries,
            fps=fps,
            features=features,
        )

        classified_segments = []
        recognized_labels = []
        spoken_outputs = []

        total_classifier_latency_ms = 0.0

        for item in extracted_segments:
            meta = item["metadata"]
            landmarks = item["landmarks"]  # (T_seg, 94, 4)

            if not meta.is_valid:
                # Segment failed duration, tracking, or NaN criteria
                classified_segments.append({
                    "segment_id": meta.segment_id,
                    "timestamps": {
                        "start_frame": meta.start_frame,
                        "end_frame": meta.end_frame,
                        "start_seconds": meta.start_timestamp,
                        "end_seconds": meta.end_timestamp,
                        "duration_seconds": meta.duration_seconds,
                    },
                    "segment_metrics": {
                        "tracking_quality": meta.tracking_quality,
                        "hand_presence_ratio": meta.hand_presence_ratio,
                    },
                    "status": "rejected_segment",
                    "rejection_reasons": meta.rejection_reasons,
                    "prediction": None,
                    "top_k": [],
                    "confidence": 0.0,
                    "spoken": False,
                })
                continue

            # Run Phase 3 Isolated Inference
            t_cls_start = time.perf_counter()
            pred_res = self.isolated_recognizer.predict_landmarks(
                raw_keypoints=landmarks,
                category=category_filter,
                top_k=top_k,
            )
            cls_ms = (time.perf_counter() - t_cls_start) * 1000.0
            total_classifier_latency_ms += cls_ms

            predicted_sign = pred_res.get("predicted_sign", "UNKNOWN")
            display_name = pred_res.get("display_name", "Unknown")
            confidence = float(pred_res.get("confidence", 0.0))
            is_valid = bool(pred_res.get("is_valid", False))
            status = pred_res.get("status", "unknown")
            top_preds = pred_res.get("top_predictions", [])
            reason = pred_res.get("reason")

            # Check vocabulary interpretation: alphabet vs word
            category = pred_res.get("category", "")
            is_alphabet = category == "alphabet"

            # TTS trigger for valid signs
            tts_res = None
            if self.enable_tts and is_valid:
                tts_res = self.tts.speak_prediction(
                    raw_text=predicted_sign,
                    is_valid=is_valid,
                    confidence=confidence,
                )
                spoken_outputs.append(tts_res.get("spoken_text"))

            if is_valid:
                recognized_labels.append(display_name)

            classified_segments.append({
                "segment_id": meta.segment_id,
                "timestamps": {
                    "start_frame": meta.start_frame,
                    "end_frame": meta.end_frame,
                    "start_seconds": meta.start_timestamp,
                    "end_seconds": meta.end_timestamp,
                    "duration_seconds": meta.duration_seconds,
                },
                "segment_metrics": {
                    "tracking_quality": meta.tracking_quality,
                    "hand_presence_ratio": meta.hand_presence_ratio,
                },
                "status": status,
                "is_valid": is_valid,
                "reason": reason,
                "predicted_sign": predicted_sign,
                "display_name": display_name,
                "category": category,
                "is_alphabet": is_alphabet,
                "confidence": confidence,
                "top_k": top_preds,
                "inference_time_ms": round(cls_ms, 2),
                "tts": tts_res,
            })

        total_latency_ms = (time.perf_counter() - t0) * 1000.0

        return {
            "mode": "Mode_A_Isolated_Segmented",
            "success": True,
            "total_frames": len(keypoints),
            "fps": fps,
            "detected_segments_count": len(raw_boundaries),
            "valid_segments_count": len([s for s in classified_segments if s.get("is_valid", False)]),
            "recognized_sequence": recognized_labels,
            "segments": classified_segments,
            "timing_ms": {
                "segmentation_ms": round(seg_latency_ms, 2),
                "classification_ms": round(total_classifier_latency_ms, 2),
                "total_pipeline_ms": round(total_latency_ms, 2),
            },
        }

    # -------------------------------------------------------------------------
    # Mode B: Continuous Sentence Translation
    # Full Video Sequence -> ISLiM Official Preprocessing -> T5 Translation
    # -------------------------------------------------------------------------
    def run_mode_b(
        self,
        full_keypoints: np.ndarray,
        fps: float = 30.0,
        decoding: str = "beam",
    ) -> Dict[str, Any]:
        """
        Executes Mode B: Full-Video Continuous Sentence Translation via ISLiM.
        Sends the complete video sequence. Detects repetitive or degenerate text.
        Does NOT invent a fake confidence score.
        """
        t0 = time.perf_counter()
        if len(full_keypoints) == 0:
            return {
                "mode": "Mode_B_Continuous_ISLiM",
                "success": False,
                "error": "Empty keypoints input.",
                "raw_prediction": "",
                "clean_text": "",
                "latency_ms": 0.0,
            }

        # Predict using full video
        pred_res = self.islim_predictor.predict(
            keypoints=full_keypoints,
            decoding=decoding,
        )
        latency_ms = (time.perf_counter() - t0) * 1000.0

        raw_pred = pred_res.get("prediction", "").strip()
        token_ids = pred_res.get("token_ids", [])

        # Quality validation on generated text
        quality_info = self._validate_islim_output(raw_pred, token_ids)

        # TTS execution if enabled and text is valid and non-degenerate
        tts_res = None
        if self.enable_tts and quality_info["is_valid"] and quality_info["clean_text"]:
            tts_res = self.tts.speak_prediction(
                raw_text=quality_info["clean_text"],
                is_valid=True,
                confidence=1.0,  # Do not invent confidence; treat non-degenerate output as speakable
            )

        return {
            "mode": "Mode_B_Continuous_ISLiM",
            "success": True,
            "total_frames": len(full_keypoints),
            "fps": fps,
            "decoding": decoding,
            "raw_prediction": raw_pred,
            "clean_text": quality_info["clean_text"],
            "token_ids": token_ids,
            "is_valid": quality_info["is_valid"],
            "quality_status": quality_info["status"],
            "quality_flags": quality_info["flags"],
            "confidence": None,  # Explicit: ISLiM does not output softmax confidence
            "latency_ms": round(latency_ms, 2),
            "tts": tts_res,
        }

    # -------------------------------------------------------------------------
    # ISLiM Output Postprocessing and Degeneracy Detection
    # -------------------------------------------------------------------------
    @staticmethod
    def _validate_islim_output(raw_text: str, token_ids: List[int]) -> Dict[str, Any]:
        """
        Detects empty, repeated, looped, or degenerate text from beam search / greedy decoding.
        Keeps display postprocessing strictly separate from raw output.
        """
        flags = []
        is_valid = True
        status = "normal"

        if not raw_text or raw_text.strip() == "":
            flags.append("empty_output")
            return {
                "is_valid": False,
                "status": "empty",
                "clean_text": "",
                "flags": flags,
            }

        words = raw_text.strip().split()
        if len(words) == 0:
            flags.append("whitespace_only")
            return {"is_valid": False, "status": "empty", "clean_text": "", "flags": flags}

        # 1. Repetition detection (e.g. "person person person")
        word_counts = Counter(words)
        most_common_word, count = word_counts.most_common(1)[0]
        if count > 4 and (count / len(words)) > 0.5:
            flags.append(f"repeated_word_loop: '{most_common_word}' appeared {count} times")
            status = "degenerate_repetition"
            is_valid = False

        # 2. Bigram loops (e.g. "is not is not is not")
        if len(words) >= 4:
            bigrams = [f"{words[i]} {words[i+1]}" for i in range(len(words) - 1)]
            bg_counts = Counter(bigrams)
            top_bg, bg_cnt = bg_counts.most_common(1)[0]
            if bg_cnt >= 3:
                flags.append(f"repeated_phrase_loop: '{top_bg}' appeared {bg_cnt} times")
                status = "degenerate_phrase_loop"
                is_valid = False

        # 3. Clean display text (removes double spaces, capitalizes sentence)
        clean_text = re.sub(r"\s+", " ", raw_text).strip()
        if len(clean_text) > 0:
            clean_text = clean_text[0].upper() + clean_text[1:]

        return {
            "is_valid": is_valid,
            "status": status,
            "clean_text": clean_text,
            "flags": flags,
        }

    # -------------------------------------------------------------------------
    # Dual Mode Orchestration
    # -------------------------------------------------------------------------
    def run_both(
        self,
        full_keypoints: np.ndarray,
        fps: float = 30.0,
        category_filter: Optional[str] = None,
        decoding: str = "beam",
    ) -> Dict[str, Any]:
        """
        Runs both Mode A (Isolated / Segmented) and Mode B (ISLiM Continuous)
        on the input sequence for comparative side-by-side analysis.
        """
        mode_a_result = self.run_mode_a(full_keypoints, fps=fps, category_filter=category_filter)
        mode_b_result = self.run_mode_b(full_keypoints, fps=fps, decoding=decoding)

        return {
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "total_frames": len(full_keypoints),
            "fps": fps,
            "mode_a_isolated": mode_a_result,
            "mode_b_continuous": mode_b_result,
        }
