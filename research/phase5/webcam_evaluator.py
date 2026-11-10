"""
Signova AI - Real-Time Camera & End-to-End Latency Evaluator (Phase 5).
Measures:
  - Camera capture FPS
  - MediaPipe landmark extraction latency (p50, p95)
  - Phase 4 segmentation latency (p50, p95)
  - Phase 3 isolated inference latency (p50, p95)
  - Phase 2 ISLiM sentence inference latency
  - End-to-end latency and processing FPS
  - Process RAM and GPU VRAM memory usage
  - CPU utilization
Supports live physical webcam (device 0) and synthetic video-stream fallback for headless testing.
"""

import ctypes
from ctypes import wintypes
import json
import logging
import os
from pathlib import Path
import sys
import time
from typing import Any, Dict, List, Optional, Tuple
import cv2
import numpy as np
import torch

# Process memory via Windows API without external dependencies
class PROCESS_MEMORY_COUNTERS(ctypes.Structure):
    _fields_ = [
        ('cb', wintypes.DWORD),
        ('PageFaultCount', wintypes.DWORD),
        ('PeakWorkingSetSize', ctypes.c_size_t),
        ('WorkingSetSize', ctypes.c_size_t),
        ('QuotaPeakPagedPoolUsage', ctypes.c_size_t),
        ('QuotaPagedPoolUsage', ctypes.c_size_t),
        ('QuotaPeakNonPagedPoolUsage', ctypes.c_size_t),
        ('QuotaNonPagedPoolUsage', ctypes.c_size_t),
        ('PagefileUsage', ctypes.c_size_t),
        ('PeakPagefileUsage', ctypes.c_size_t),
    ]

def get_process_ram_mb() -> float:
    try:
        kernel32 = ctypes.windll.kernel32
        psapi = ctypes.windll.psapi
        kernel32.GetCurrentProcess.restype = wintypes.HANDLE
        psapi.GetProcessMemoryInfo.argtypes = [wintypes.HANDLE, ctypes.c_void_p, wintypes.DWORD]
        psapi.GetProcessMemoryInfo.restype = wintypes.BOOL

        counters = PROCESS_MEMORY_COUNTERS()
        counters.cb = ctypes.sizeof(PROCESS_MEMORY_COUNTERS)
        handle = kernel32.GetCurrentProcess()
        if psapi.GetProcessMemoryInfo(handle, ctypes.byref(counters), counters.cb):
            return round(counters.WorkingSetSize / (1024 * 1024), 2)
    except Exception:
        pass
    return 0.0

def get_process_cpu_time() -> float:
    try:
        kernel32 = ctypes.windll.kernel32
        kernel32.GetCurrentProcess.restype = wintypes.HANDLE
        kernel32.GetProcessTimes.argtypes = [
            wintypes.HANDLE,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
            ctypes.c_void_p,
        ]
        kernel32.GetProcessTimes.restype = wintypes.BOOL

        creation_time = wintypes.FILETIME()
        exit_time = wintypes.FILETIME()
        kernel_time = wintypes.FILETIME()
        user_time = wintypes.FILETIME()
        handle = kernel32.GetCurrentProcess()
        if kernel32.GetProcessTimes(
            handle,
            ctypes.byref(creation_time),
            ctypes.byref(exit_time),
            ctypes.byref(kernel_time),
            ctypes.byref(user_time),
        ):
            k_us = (kernel_time.dwHighDateTime << 32) + kernel_time.dwLowDateTime
            u_us = (user_time.dwHighDateTime << 32) + user_time.dwLowDateTime
            return (k_us + u_us) / 10000000.0  # seconds
    except Exception:
        pass
    return 0.0

# Ensure paths in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ISLIM_DIR = PROJECT_ROOT / "research" / "ISLiM"
RESEARCH_DIR = PROJECT_ROOT / "research"
BACKEND_DIR = PROJECT_ROOT / "backend"

for p in [str(PROJECT_ROOT), str(RESEARCH_DIR), str(ISLIM_DIR), str(BACKEND_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from research.phase5.orchestrator import SignovaOrchestrator
from research.phase5.tts_module import SignovaTTS
from research.video_pipeline.landmark_extractor import MediaPipeLandmarkExtractor
from backend.app.ml.recognition.sign_segmentation import SignSegmentationBuffer

logger = logging.getLogger("signova.phase5.webcam")


class WebcamEvaluator:
    """
    Evaluates live camera pipeline timing, latency percentiles, and memory footprint.
    """

    def __init__(
        self,
        camera_id: int = 0,
        synthetic_video_path: Optional[Path] = None,
        max_eval_frames: int = 90,
        target_fps: float = 30.0,
        device: str = "auto",
        enable_tts: bool = True,
    ) -> None:
        self.camera_id = camera_id
        self.synthetic_video_path = synthetic_video_path or (
            PROJECT_ROOT / "vidssavecom-president-prime-minister-chief-minister-indian-sign-language-i_KWDwb1ih.mp4"
        )
        self.max_eval_frames = max_eval_frames
        self.target_fps = target_fps
        self.device = device
        self.enable_tts = enable_tts

        self.orchestrator = SignovaOrchestrator(
            device=device,
            enable_tts=enable_tts,
        )
        self.extractor = MediaPipeLandmarkExtractor()
        self.streaming_buffer = SignSegmentationBuffer(window_size=30)
        self.start_cpu_time = get_process_cpu_time()

    def run_evaluation(self) -> Dict[str, Any]:
        """
        Executes end-to-end camera pipeline benchmark and records latency percentiles.
        """
        # Memory baseline before run
        ram_before_mb = get_process_ram_mb()
        vram_before_mb = torch.cuda.memory_allocated() / (1024 * 1024) if torch.cuda.is_available() else 0.0

        # Attempt to open physical camera
        cap = cv2.VideoCapture(self.camera_id)
        is_synthetic = False
        source_name = f"Physical Webcam (ID {self.camera_id})"

        if not cap.isOpened():
            logger.info("Physical camera %d unavailable. Using video-stream simulation: %s", self.camera_id, self.synthetic_video_path.name)
            cap.release()
            cap = cv2.VideoCapture(str(self.synthetic_video_path))
            is_synthetic = True
            source_name = f"Simulated Camera Stream ({self.synthetic_video_path.name})"
            if not cap.isOpened():
                raise RuntimeError(f"Cannot initialize camera or fallback video: {self.synthetic_video_path}")

        # Metrics trackers
        capture_times_ms: List[float] = []
        extraction_times_ms: List[float] = []
        segmentation_times_ms: List[float] = []
        isolated_times_ms: List[float] = []
        e2e_frame_times_ms: List[float] = []

        all_landmarks: List[np.ndarray] = []
        triggered_gestures: List[Dict[str, Any]] = []

        frames_processed = 0
        t_session_start = time.perf_counter()

        # Initial CPU time
        cpu_t0 = get_process_cpu_time()

        try:
            while frames_processed < self.max_eval_frames:
                t_frame_start = time.perf_counter()

                # 1. Camera Frame Capture
                t_cap_start = time.perf_counter()
                ret, frame = cap.read()
                if not ret:
                    if is_synthetic:
                        # Loop video for continuous testing
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        ret, frame = cap.read()
                        if not ret:
                            break
                    else:
                        break
                capture_ms = (time.perf_counter() - t_cap_start) * 1000.0
                capture_times_ms.append(capture_ms)

                # Convert to RGB
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # 2. MediaPipe Holistic 94-Landmark Extraction
                t_ext_start = time.perf_counter()
                kp, _ = self.extractor.extract_frame(rgb_frame)  # (94, 4)
                extraction_ms = (time.perf_counter() - t_ext_start) * 1000.0
                extraction_times_ms.append(extraction_ms)
                all_landmarks.append(kp)

                # 3. Live Streaming Segmentation
                t_seg_start = time.perf_counter()
                completed_seq = self.streaming_buffer.add_frame(kp)
                seg_ms = (time.perf_counter() - t_seg_start) * 1000.0
                segmentation_times_ms.append(seg_ms)

                # 4. Phase 3 Isolated Inference upon gesture trigger
                if completed_seq is not None:
                    t_iso_start = time.perf_counter()
                    iso_res = self.orchestrator.isolated_recognizer.predict_landmarks(
                        raw_keypoints=completed_seq,
                        top_k=3,
                    )
                    iso_ms = (time.perf_counter() - t_iso_start) * 1000.0
                    isolated_times_ms.append(iso_ms)

                    # Trigger TTS if enabled
                    if self.enable_tts and iso_res.get("is_valid", False):
                        self.orchestrator.tts.speak_prediction(
                            raw_text=iso_res.get("predicted_sign", ""),
                            is_valid=True,
                            confidence=iso_res.get("confidence", 0.0),
                        )

                    triggered_gestures.append({
                        "frame_index": frames_processed,
                        "predicted_sign": iso_res.get("predicted_sign"),
                        "display_name": iso_res.get("display_name"),
                        "confidence": iso_res.get("confidence"),
                        "status": iso_res.get("status"),
                        "is_valid": iso_res.get("is_valid"),
                        "inference_latency_ms": round(iso_ms, 2),
                    })

                e2e_ms = (time.perf_counter() - t_frame_start) * 1000.0
                e2e_frame_times_ms.append(e2e_ms)
                frames_processed += 1

        finally:
            cap.release()

        total_elapsed_s = time.perf_counter() - t_session_start
        overall_processing_fps = frames_processed / max(0.001, total_elapsed_s)
        mean_cap_ms = float(np.mean(capture_times_ms)) if capture_times_ms else 0.0
        capture_fps = 1000.0 / mean_cap_ms if mean_cap_ms > 0 else 0.0

        # 5. Measure Full-Sequence ISLiM Inference Latency
        islim_latency_ms = None
        islim_pred = None
        if len(all_landmarks) > 10:
            accumulated_kps = np.array(all_landmarks, dtype=np.float32)
            t_islim_start = time.perf_counter()
            islim_res = self.orchestrator.run_mode_b(accumulated_kps, fps=self.target_fps, decoding="beam")
            islim_latency_ms = (time.perf_counter() - t_islim_start) * 1000.0
            islim_pred = islim_res.get("clean_text")

        # Memory and Resource Profiling
        ram_peak_mb = get_process_ram_mb()
        vram_peak_mb = torch.cuda.max_memory_allocated() / (1024 * 1024) if torch.cuda.is_available() else 0.0
        cpu_spent = get_process_cpu_time() - cpu_t0
        cpu_utilization = (cpu_spent / max(0.001, total_elapsed_s)) * 100.0

        gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "CPU"

        return {
            "source_type": source_name,
            "is_synthetic": is_synthetic,
            "frames_evaluated": frames_processed,
            "total_elapsed_seconds": round(total_elapsed_s, 2),
            "camera_capture_fps": round(capture_fps, 2),
            "processing_fps": round(overall_processing_fps, 2),
            "latencies_ms": {
                "capture": {
                    "mean": round(float(np.mean(capture_times_ms)), 2),
                    "p50": round(float(np.percentile(capture_times_ms, 50)), 2),
                    "p95": round(float(np.percentile(capture_times_ms, 95)), 2),
                },
                "mediapipe_extraction": {
                    "mean": round(float(np.mean(extraction_times_ms)), 2),
                    "p50": round(float(np.percentile(extraction_times_ms, 50)), 2),
                    "p95": round(float(np.percentile(extraction_times_ms, 95)), 2),
                },
                "segmentation_step": {
                    "mean": round(float(np.mean(segmentation_times_ms)), 2),
                    "p50": round(float(np.percentile(segmentation_times_ms, 50)), 2),
                    "p95": round(float(np.percentile(segmentation_times_ms, 95)), 2),
                },
                "phase3_isolated_inference": {
                    "count": len(isolated_times_ms),
                    "mean": round(float(np.mean(isolated_times_ms)), 2) if isolated_times_ms else 0.0,
                    "p50": round(float(np.percentile(isolated_times_ms, 50)), 2) if isolated_times_ms else 0.0,
                    "p95": round(float(np.percentile(isolated_times_ms, 95)), 2) if isolated_times_ms else 0.0,
                },
                "phase2_islim_full_sequence": {
                    "latency_ms": round(islim_latency_ms, 2) if islim_latency_ms else None,
                    "prediction": islim_pred,
                },
                "end_to_end_per_frame": {
                    "mean": round(float(np.mean(e2e_frame_times_ms)), 2),
                    "p50": round(float(np.percentile(e2e_frame_times_ms, 50)), 2),
                    "p95": round(float(np.percentile(e2e_frame_times_ms, 95)), 2),
                },
            },
            "resources": {
                "device": self.device,
                "gpu_hardware": gpu_name,
                "ram_baseline_mb": round(ram_before_mb, 1),
                "ram_peak_mb": round(ram_peak_mb, 1),
                "vram_baseline_mb": round(vram_before_mb, 1),
                "vram_peak_mb": round(vram_peak_mb, 1),
                "cpu_utilization_pct": round(cpu_utilization, 1),
            },
            "triggered_gestures": triggered_gestures,
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    evaluator = WebcamEvaluator(max_eval_frames=60, enable_tts=True)
    report = evaluator.run_evaluation()
    print(json.dumps(report, indent=2))
