"""
Integrated Video-to-ISLiM Inference Pipeline (Part 2.2).

Composes:
1. Video reading & MediaPipe 94-landmark extraction (Part 2.1 VideoProcessor).
2. ISLiM pretrained visual-encoder + T5 autoregressive translation (Part 1.9 ISLiMPredictor).
"""

from pathlib import Path
import sys
import time
from typing import Any, Dict, Optional, Tuple, Union
import numpy as np
import torch

# Ensure ISLiM is importable
PIPELINE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PIPELINE_DIR.parent.parent
ISLIM_DIR = PROJECT_ROOT / "research" / "ISLiM"
if str(ISLIM_DIR) not in sys.path:
    sys.path.insert(0, str(ISLIM_DIR))

try:
    from research.ISLiM.inference.predictor import ISLiMPredictor
except ImportError:
    from inference.predictor import ISLiMPredictor  # type: ignore[import-not-found]
try:
    from research.video_pipeline.config import VideoPipelineConfig
    from research.video_pipeline.output_handler import save_json_report, save_keypoints
    from research.video_pipeline.video_processor import VideoProcessor
except ImportError:
    from .config import VideoPipelineConfig
    from .output_handler import save_json_report, save_keypoints
    from .video_processor import VideoProcessor

DEFAULT_PART2_2_RESULTS_DIR = PIPELINE_DIR / "results_part2_2"


class VideoToISLiMPipeline:
    """
    End-to-end video-to-sign-language translation pipeline.
    Loads ISLiM model once upon instantiation and reuses it across videos.
    """

    def __init__(
        self,
        checkpoint_path: Optional[Union[str, Path]] = None,
        tokenizer_dir: Optional[Union[str, Path]] = None,
        device: str = "auto",
        video_config: Optional[VideoPipelineConfig] = None,
        results_dir: Optional[Union[str, Path]] = None,
    ):
        self.video_config = video_config or VideoPipelineConfig()
        self.results_dir = Path(results_dir or DEFAULT_PART2_2_RESULTS_DIR).resolve()
        self.results_dir.mkdir(parents=True, exist_ok=True)

        # 1. Initialize video processor (MediaPipe extractor initialized per video or reused)
        self.video_processor = VideoProcessor(self.video_config)

        # 2. Load ISLiM model and tokenizer ONCE upon initialization
        self.predictor = ISLiMPredictor(
            checkpoint_path=checkpoint_path,
            tokenizer_dir=tokenizer_dir,
            device=device,
        )
        self.device = self.predictor.device

    def predict_video(
        self,
        video_path: Union[str, Path],
        decoding: str = "beam",
        max_length: int = 128,
        num_beams: int = 4,
        repetition_penalty: float = 1.5,
        no_repeat_ngram_size: int = 3,
        length_penalty: float = 1.2,
        save_output: bool = True,
        output_dir: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """
        Execute end-to-end translation from video file to English text.

        Returns:
            Dictionary containing prediction text, tokens, extraction stats, and timings.
        """
        target_video = Path(video_path).resolve()
        save_dir = Path(output_dir or self.results_dir).resolve()
        save_dir.mkdir(parents=True, exist_ok=True)

        if not target_video.exists():
            raise FileNotFoundError(f"Target video not found: {target_video}")

        # Reset GPU peak memory tracking if CUDA available
        if self.device.type == "cuda":
            torch.cuda.reset_peak_memory_stats(self.device)

        t_total_start = time.perf_counter()

        # Step 1: Video decoding and landmark extraction (T, 94, 4)
        t_extract_start = time.perf_counter()
        raw_keypoints, extraction_report = self.video_processor.process_video(
            video_path=target_video,
            save_output=False,
        )
        t_extract_end = time.perf_counter()
        extraction_time_ms = (t_extract_end - t_extract_start) * 1000.0

        # Step 2: ISLiM preprocessing + model generation (reusing loaded model)
        pred_result = self.predictor.predict(
            keypoints=raw_keypoints,
            decoding=decoding,
            max_length=max_length,
            num_beams=num_beams,
            repetition_penalty=repetition_penalty,
            no_repeat_ngram_size=no_repeat_ngram_size,
            length_penalty=length_penalty,
        )

        t_total_end = time.perf_counter()
        total_time_ms = (t_total_end - t_total_start) * 1000.0

        # Capture peak GPU memory
        peak_vram_mb = None
        if self.device.type == "cuda":
            peak_vram_mb = round(torch.cuda.max_memory_allocated(self.device) / (1024 * 1024), 2)

        video_stem = target_video.stem
        npy_path = save_dir / f"{video_stem}_keypoints.npy"
        report_path = save_dir / f"{video_stem}_inference_report.json"

        # Format comprehensive result
        result: Dict[str, Any] = {
            "input_video_filename": target_video.name,
            "input_video_path": str(target_video),
            "video_duration_seconds": extraction_report["video_duration_seconds"],
            "fps": extraction_report["fps"],
            "resolution": extraction_report["resolution"],
            "extracted_frame_count": extraction_report["processed_frames"],
            "landmark_shape": list(raw_keypoints.shape),
            "landmark_dtype": str(raw_keypoints.dtype),
            "subsystem_detection_rates": extraction_report["subsystem_detection_rates"],
            "landmark_presence_percentage": extraction_report["landmark_presence_percentage"],
            "decoding_strategy": decoding,
            "prediction": pred_result["prediction"],
            "token_ids": pred_result["token_ids"],
            "timings": {
                "landmark_extraction_time_ms": round(extraction_time_ms, 2),
                "preprocessing_time_ms": round(pred_result["preprocessing_time_ms"], 2),
                "model_inference_time_ms": round(pred_result["inference_time_ms"], 2),
                "total_processing_time_ms": round(total_time_ms, 2),
                "total_processing_time_seconds": round(total_time_ms / 1000.0, 3),
            },
            "device": {
                "type": self.device.type,
                "name": torch.cuda.get_device_name(self.device) if self.device.type == "cuda" else "CPU",
                "peak_vram_mb": peak_vram_mb,
            },
            "output_status": "SUCCESS",
            "semantic_accuracy_status": "UNVERIFIED (No verified reference subtitle provided for evaluation)",
        }

        if save_output:
            save_keypoints(raw_keypoints, npy_path)
            save_json_report(result, report_path)
            result["saved_keypoints_path"] = str(npy_path)
            result["saved_report_path"] = str(report_path)

        return result

    def predict_video_both_decodings(
        self,
        video_path: Union[str, Path],
        save_output: bool = True,
        output_dir: Optional[Union[str, Path]] = None,
    ) -> Dict[str, Any]:
        """
        Process video once and run both beam search and greedy decoding.
        Prevents redundant video decoding and landmark extraction.
        """
        target_video = Path(video_path).resolve()
        save_dir = Path(output_dir or self.results_dir).resolve()
        save_dir.mkdir(parents=True, exist_ok=True)

        if self.device.type == "cuda":
            torch.cuda.reset_peak_memory_stats(self.device)

        t_total_start = time.perf_counter()

        # Step 1: Extract landmarks once
        t_extract_start = time.perf_counter()
        raw_keypoints, extraction_report = self.video_processor.process_video(
            video_path=target_video,
            save_output=False,
        )
        t_extract_end = time.perf_counter()
        extraction_time_ms = (t_extract_end - t_extract_start) * 1000.0

        # Step 2: Beam search (B=4)
        beam_pred = self.predictor.predict(
            keypoints=raw_keypoints,
            decoding="beam",
            num_beams=4,
        )

        # Step 3: Greedy search (B=1)
        greedy_pred = self.predictor.predict(
            keypoints=raw_keypoints,
            decoding="greedy",
            num_beams=1,
        )

        t_total_end = time.perf_counter()
        total_time_ms = (t_total_end - t_total_start) * 1000.0

        peak_vram_mb = None
        if self.device.type == "cuda":
            peak_vram_mb = round(torch.cuda.max_memory_allocated(self.device) / (1024 * 1024), 2)

        video_stem = target_video.stem
        npy_path = save_dir / f"{video_stem}_keypoints.npy"
        report_path = save_dir / f"{video_stem}_inference_report.json"

        combined_report: Dict[str, Any] = {
            "input_video_filename": target_video.name,
            "input_video_path": str(target_video),
            "video_duration_seconds": extraction_report["video_duration_seconds"],
            "fps": extraction_report["fps"],
            "resolution": extraction_report["resolution"],
            "extracted_frame_count": extraction_report["processed_frames"],
            "landmark_shape": list(raw_keypoints.shape),
            "landmark_dtype": str(raw_keypoints.dtype),
            "subsystem_detection_rates": extraction_report["subsystem_detection_rates"],
            "landmark_presence_percentage": extraction_report["landmark_presence_percentage"],
            "beam_search": {
                "num_beams": 4,
                "prediction": beam_pred["prediction"],
                "token_ids": beam_pred["token_ids"],
                "inference_time_ms": round(beam_pred["inference_time_ms"], 2),
            },
            "greedy_search": {
                "num_beams": 1,
                "prediction": greedy_pred["prediction"],
                "token_ids": greedy_pred["token_ids"],
                "inference_time_ms": round(greedy_pred["inference_time_ms"], 2),
            },
            "timings": {
                "landmark_extraction_time_ms": round(extraction_time_ms, 2),
                "preprocessing_time_ms": round(beam_pred["preprocessing_time_ms"], 2),
                "beam_inference_time_ms": round(beam_pred["inference_time_ms"], 2),
                "greedy_inference_time_ms": round(greedy_pred["inference_time_ms"], 2),
                "total_processing_time_ms": round(total_time_ms, 2),
                "total_processing_time_seconds": round(total_time_ms / 1000.0, 3),
            },
            "device": {
                "type": self.device.type,
                "name": torch.cuda.get_device_name(self.device) if self.device.type == "cuda" else "CPU",
                "peak_vram_mb": peak_vram_mb,
            },
            "output_status": "SUCCESS",
            "semantic_accuracy_status": "UNVERIFIED (No verified reference subtitle provided for evaluation)",
        }

        if save_output:
            save_keypoints(raw_keypoints, npy_path)
            save_json_report(combined_report, report_path)
            combined_report["saved_keypoints_path"] = str(npy_path)
            combined_report["saved_report_path"] = str(report_path)

        return combined_report
