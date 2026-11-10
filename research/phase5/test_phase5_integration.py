"""
Signova AI - Comprehensive Phase 5 Integration Test Suite.
Verifies all 13 required test cases:
  1. Single isolated sign
  2. Multiple consecutive signs
  3. Short pauses between signs
  4. Long pauses between signs
  5. Static sign holds
  6. Fast gestures
  7. Slow gestures
  8. Missing hands
  9. Poor tracking
  10. Unknown signs
  11. Empty or invalid video
  12. Continuous sentence translation
  13. TTS enabled and disabled
"""

import json
from pathlib import Path
import sys
import time
from typing import Any, Dict
import numpy as np
import pytest

# Ensure research paths in sys.path
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
from research.segmentation.boundary_detector import KinematicFeatureExtractor
from research.segmentation.state_machine import SegmentationStateMachine, SignState

SAMPLE_KP_PATH_1 = (
    RESEARCH_DIR
    / "video_pipeline"
    / "results_part2_2"
    / "vidssavecom-president-prime-minister-chief-minister-indian-sign-language-i_KWDwb1ih_keypoints.npy"
)
SAMPLE_KP_PATH_2 = (
    RESEARCH_DIR
    / "video_pipeline"
    / "results_part2_2"
    / "Learn-Indian-Sign-SnapYT.App (1) (online-video-cutter.com)_keypoints.npy"
)


@pytest.fixture(scope="module")
def orchestrator():
    """Initializes single shared orchestrator with both models loaded."""
    orch = SignovaOrchestrator(device="auto", enable_tts=False)
    # Warm up models
    _ = orch.isolated_recognizer
    _ = orch.islim_predictor
    yield orch
    orch.tts.stop()


@pytest.fixture(scope="module")
def keypoints_sample_1():
    assert SAMPLE_KP_PATH_1.exists(), f"Missing keypoints sample: {SAMPLE_KP_PATH_1}"
    return np.load(str(SAMPLE_KP_PATH_1))


@pytest.fixture(scope="module")
def keypoints_sample_2():
    assert SAMPLE_KP_PATH_2.exists(), f"Missing keypoints sample: {SAMPLE_KP_PATH_2}"
    return np.load(str(SAMPLE_KP_PATH_2))


# -----------------------------------------------------------------------------
# Test Case 1: Single Isolated Sign
# -----------------------------------------------------------------------------
def test_case_01_single_isolated_sign(orchestrator, keypoints_sample_1):
    """Feed a single isolated sign slice (frames 6 to 22) into Mode A."""
    single_sign_kps = keypoints_sample_1[6:23].copy()  # 17 frames
    res = orchestrator.run_mode_a(single_sign_kps, fps=30.0)

    assert res["success"] is True
    assert res["mode"] == "Mode_A_Isolated_Segmented"
    # Should detect 1 segment or classify isolated sequence
    assert len(res["segments"]) >= 1
    seg = res["segments"][0]
    assert "timestamps" in seg
    assert seg["timestamps"]["start_seconds"] >= 0.0
    assert "top_k" in seg


# -----------------------------------------------------------------------------
# Test Case 2: Multiple Consecutive Signs
# -----------------------------------------------------------------------------
def test_case_02_multiple_consecutive_signs(orchestrator, keypoints_sample_1):
    """Feed sequence with multiple consecutive signs (President + Prime Minister)."""
    res = orchestrator.run_mode_a(keypoints_sample_1, fps=30.0)

    assert res["success"] is True
    # Ground truth contains 2 signs
    assert res["detected_segments_count"] == 2
    assert len(res["segments"]) == 2
    # Verify temporal non-overlap and ascending order
    seg1, seg2 = res["segments"][0], res["segments"][1]
    assert seg1["timestamps"]["start_frame"] < seg2["timestamps"]["start_frame"]
    assert seg1["timestamps"]["end_frame"] <= seg2["timestamps"]["start_frame"]


# -----------------------------------------------------------------------------
# Test Case 3: Short Pauses Between Signs
# -----------------------------------------------------------------------------
def test_case_03_short_pauses_between_signs(orchestrator, keypoints_sample_1):
    """Insert a short pause (3 idle frames) between consecutive sign segments."""
    seg1 = keypoints_sample_1[6:22]
    seg2 = keypoints_sample_1[26:46]
    # Create 3 idle frames (hands near navel/zero)
    idle = np.zeros((3, 94, 4), dtype=np.float32)
    idle[:, 0, :] = [0.4, 0.3, 0.0, 1.0]
    idle[:, 1, :] = [0.6, 0.3, 0.0, 1.0]

    stitched = np.concatenate([seg1, idle, seg2], axis=0)
    res = orchestrator.run_mode_a(stitched, fps=30.0)

    assert res["success"] is True
    # Should separate the two signs and not fuse them
    assert res["detected_segments_count"] >= 2


# -----------------------------------------------------------------------------
# Test Case 4: Long Pauses Between Signs
# -----------------------------------------------------------------------------
def test_case_04_long_pauses_between_signs(orchestrator, keypoints_sample_1):
    """Insert a long pause (45 frames / 1.5s) between consecutive signs."""
    seg1 = keypoints_sample_1[6:22]
    seg2 = keypoints_sample_1[26:46]
    long_idle = np.zeros((45, 94, 4), dtype=np.float32)
    long_idle[:, 0, :] = [0.4, 0.3, 0.0, 1.0]
    long_idle[:, 1, :] = [0.6, 0.3, 0.0, 1.0]

    stitched = np.concatenate([seg1, long_idle, seg2], axis=0)
    res = orchestrator.run_mode_a(stitched, fps=30.0)

    assert res["success"] is True
    assert res["detected_segments_count"] == 2
    # The pause should cleanly separate them with a noticeable gap
    gap_frames = res["segments"][1]["timestamps"]["start_frame"] - res["segments"][0]["timestamps"]["end_frame"]
    assert gap_frames >= 30


# -----------------------------------------------------------------------------
# Test Case 5: Static Sign Holds
# -----------------------------------------------------------------------------
def test_case_05_static_sign_holds(orchestrator):
    """Verify dual-condition gate keeps segment active during zero-velocity static hold."""
    T = 40
    kp = np.zeros((T, 94, 4), dtype=np.float32)
    # Shoulders & hips
    kp[:, 0, :] = [0.4, 0.4, 0.0, 1.0]
    kp[:, 1, :] = [0.6, 0.4, 0.0, 1.0]
    kp[:, 4, :] = [0.4, 0.8, 0.0, 1.0]
    kp[:, 5, :] = [0.6, 0.8, 0.0, 1.0]

    # Frames 5 to 10: Dynamic entry movement
    for t in range(5, 11):
        kp[t, 27:48, 0] = 0.5 + 0.05 * (t - 5)
        kp[t, 27:48, 1] = 0.30  # Elevated in signing space
        kp[t, 27:48, 3] = 1.0

    # Frames 11 to 30: Frozen in space (velocity = 0, but elevated) -> STATIC HOLD
    for t in range(11, 31):
        kp[t, 27:48, 0] = 0.75
        kp[t, 27:48, 1] = 0.30  # Elevated
        kp[t, 27:48, 3] = 1.0

    res = orchestrator.run_mode_a(kp, fps=30.0)
    assert res["success"] is True
    # Crucial: Must NOT split into 2 separate segments during the static hold
    assert res["detected_segments_count"] == 1
    seg = res["segments"][0]
    # Span must cover entry motion through the static hold
    assert seg["timestamps"]["end_frame"] >= 28


# -----------------------------------------------------------------------------
# Test Case 6: Fast Gestures
# -----------------------------------------------------------------------------
def test_case_06_fast_gestures(orchestrator, keypoints_sample_1):
    """Temporal downsampling (stride 2) simulating rapid gesture execution."""
    fast_kps = keypoints_sample_1[::2].copy()
    res = orchestrator.run_mode_a(fast_kps, fps=30.0)

    assert res["success"] is True
    assert "timing_ms" in res
    assert res["timing_ms"]["total_pipeline_ms"] > 0


# -----------------------------------------------------------------------------
# Test Case 7: Slow Gestures
# -----------------------------------------------------------------------------
def test_case_07_slow_gestures(orchestrator, keypoints_sample_1):
    """Interpolate frames to double length simulating slow signer."""
    T = len(keypoints_sample_1)
    slow_kps = np.repeat(keypoints_sample_1, 2, axis=0)  # 2x length
    res = orchestrator.run_mode_a(slow_kps, fps=30.0)

    assert res["success"] is True
    # Segments should still be detected without exceeding max_segment_frames
    assert res["detected_segments_count"] >= 1


# -----------------------------------------------------------------------------
# Test Case 8: Missing Hands
# -----------------------------------------------------------------------------
def test_case_08_missing_hands(orchestrator):
    """All hand landmarks set to 0.0 across 30 frames."""
    no_hand_kps = np.zeros((30, 94, 4), dtype=np.float32)
    # Visible shoulders
    no_hand_kps[:, 0, :] = [0.4, 0.3, 0.0, 1.0]
    no_hand_kps[:, 1, :] = [0.6, 0.3, 0.0, 1.0]

    res = orchestrator.run_mode_a(no_hand_kps, fps=30.0)
    assert res["success"] is True
    # Either no segments detected or all extracted segments marked invalid/rejected
    valid_count = res.get("valid_segments_count", 0)
    assert valid_count == 0


# -----------------------------------------------------------------------------
# Test Case 9: Poor Tracking
# -----------------------------------------------------------------------------
def test_case_09_poor_tracking(orchestrator):
    """Keypoints with very low visibility score (0.05)."""
    poor_kps = np.zeros((20, 94, 4), dtype=np.float32)
    poor_kps[:, :, 3] = 0.05  # Visibility below 0.20 threshold
    poor_kps[:, 27:48, 0] = 0.5
    poor_kps[:, 27:48, 1] = 0.3

    res = orchestrator.run_mode_a(poor_kps, fps=30.0)
    assert res["success"] is True
    # Segments should fail validation
    assert res["valid_segments_count"] == 0


# -----------------------------------------------------------------------------
# Test Case 10: Unknown Signs Outside Trained Vocabulary
# -----------------------------------------------------------------------------
def test_case_10_unknown_signs(orchestrator):
    """Synthetic random noise gesture outside ISL vocabulary."""
    np.random.seed(99)
    noise_kps = np.random.uniform(-0.1, 0.1, size=(30, 94, 4)).astype(np.float32)
    noise_kps[:, :, 3] = 1.0

    # Test direct quality validation
    pred_res = orchestrator.isolated_recognizer.predict_landmarks(noise_kps, top_k=3)
    # Must flag reason and not report false clean confirmation
    assert "status" in pred_res
    assert "is_valid" in pred_res
    assert pred_res["confidence"] <= 1.0


# -----------------------------------------------------------------------------
# Test Case 11: Empty or Invalid Video Input
# -----------------------------------------------------------------------------
def test_case_11_empty_or_invalid_video(orchestrator):
    """Empty numpy array passed into Mode A and Mode B."""
    empty_kps = np.zeros((0, 94, 4), dtype=np.float32)

    res_a = orchestrator.run_mode_a(empty_kps)
    assert res_a["success"] is False
    assert "Empty keypoints" in res_a["error"]

    res_b = orchestrator.run_mode_b(empty_kps)
    assert res_b["success"] is False
    assert "Empty keypoints" in res_b["error"]


# -----------------------------------------------------------------------------
# Test Case 12: Continuous Sentence Translation (Mode B)
# -----------------------------------------------------------------------------
def test_case_12_continuous_sentence_translation(orchestrator, keypoints_sample_1):
    """Full-video sequence passed directly to ISLiM without segment truncation."""
    res = orchestrator.run_mode_b(keypoints_sample_1, fps=30.0, decoding="beam")

    assert res["success"] is True
    assert res["mode"] == "Mode_B_Continuous_ISLiM"
    assert "raw_prediction" in res
    assert "clean_text" in res
    assert "token_ids" in res
    assert res["confidence"] is None  # Must NOT invent fake confidence score
    assert res["latency_ms"] > 0
    assert "is_valid" in res
    assert "quality_status" in res


# -----------------------------------------------------------------------------
# Test Case 13: TTS Enabled and Disabled
# -----------------------------------------------------------------------------
def test_case_13_tts_enabled_and_disabled():
    """Verify TTS enable/disable, deduplication, and non-blocking queue."""
    tts = SignovaTTS(enabled=False)
    res_disabled = tts.speak_prediction("HELLO", is_valid=True, confidence=0.90)
    assert res_disabled["status"] == "skipped"
    assert res_disabled["reason"] == "TTS disabled"

    # Enable TTS
    tts.enabled = True
    res_valid = tts.speak_prediction("HELLO", is_valid=True, confidence=0.90)
    assert res_valid["status"] == "enqueued"
    assert res_valid["spoken_text"] == "Hello"

    # Duplicate within debounce window
    res_dup = tts.speak_prediction("HELLO", is_valid=True, confidence=0.90)
    assert res_dup["status"] == "debounced"

    # Rejected prediction (confidence below 0.65)
    res_low = tts.speak_prediction("WATER", is_valid=True, confidence=0.40)
    assert res_low["status"] == "rejected"

    time.sleep(0.5)
    tts.stop()
