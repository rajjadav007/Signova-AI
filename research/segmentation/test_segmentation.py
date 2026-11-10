"""
Unit and integration tests for Continuous Sign Segmentation pipeline (Phase 4).
"""

from pathlib import Path
import sys
import numpy as np
import pytest

# Ensure research paths in sys.path
SCRIPT_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = SCRIPT_DIR.parent.parent
ISLIM_DIR = PROJECT_ROOT / "research" / "ISLiM"
RESEARCH_DIR = PROJECT_ROOT / "research"

for p in [str(PROJECT_ROOT), str(RESEARCH_DIR), str(ISLIM_DIR)]:
    if p not in sys.path:
        sys.path.insert(0, p)

from research.segmentation.boundary_detector import (
    ContinuousSignSegmenter,
    KinematicFeatureExtractor,
)
from research.segmentation.config import SegmentationConfig
from research.segmentation.evaluator import SegmentationEvaluator
from research.segmentation.segment_extractor import SegmentExtractor
from research.segmentation.state_machine import SegmentationStateMachine, SignState


def test_state_machine_transitions():
    """Verify state transitions including start confirmation, hold, and end confirmation."""
    sm = SegmentationStateMachine(
        start_confirmation_frames=2,
        end_confirmation_frames=3,
        min_segment_frames=4,
        max_segment_frames=100,
    )
    assert sm.current_state == SignState.IDLE

    # Frame 0: active motion detected -> SIGN_STARTED
    st, seg = sm.step(frame_idx=0, is_active=True, is_static_hold=False)
    assert st == SignState.SIGN_STARTED
    assert seg is None

    # Frame 1: active motion continues -> SIGN_IN_PROGRESS
    st, seg = sm.step(frame_idx=1, is_active=True, is_static_hold=False)
    assert st == SignState.SIGN_IN_PROGRESS
    assert seg is None

    # Frame 2: static hold (velocity low, but held in space) -> stays in SIGN_IN_PROGRESS
    st, seg = sm.step(frame_idx=2, is_active=False, is_static_hold=True)
    assert st == SignState.SIGN_IN_PROGRESS

    # Frame 3: active again -> SIGN_IN_PROGRESS
    st, seg = sm.step(frame_idx=3, is_active=True, is_static_hold=False)
    assert st == SignState.SIGN_IN_PROGRESS

    # Frame 4: motion stops -> POSSIBLE_SIGN_END
    st, seg = sm.step(frame_idx=4, is_active=False, is_static_hold=False)
    assert st == SignState.POSSIBLE_SIGN_END
    assert seg is None

    # Frame 5: idle continues
    st, seg = sm.step(frame_idx=5, is_active=False, is_static_hold=False)
    assert st == SignState.POSSIBLE_SIGN_END

    # Frame 6: 3rd idle frame reaches end_confirmation_frames -> SIGN_COMPLETED
    st, seg = sm.step(frame_idx=6, is_active=False, is_static_hold=False)
    assert st == SignState.SIGN_COMPLETED
    assert seg is not None
    # Segment started at frame 0, ended at frame 4 (6 - 3 + 1 = 4)
    assert seg == (0, 4)


def test_state_machine_noise_rejection():
    """Verify isolated 1-frame noise spike in IDLE does not trigger a segment."""
    sm = SegmentationStateMachine(start_confirmation_frames=2, end_confirmation_frames=3)
    # Frame 0: noise spike
    st, _ = sm.step(frame_idx=0, is_active=True)
    assert st == SignState.SIGN_STARTED

    # Frame 1: back to idle -> should abort back to IDLE
    st, seg = sm.step(frame_idx=1, is_active=False)
    assert st == SignState.IDLE
    assert seg is None
    assert len(sm.completed_segments) == 0


def test_feature_extractor_synthetic():
    """Verify feature extraction calculation on controlled synthetic keypoints."""
    T = 20
    kp = np.zeros((T, 94, 4), dtype=np.float32)

    # Set shoulders (0, 1) and hips (4, 5)
    kp[:, 0, :] = [0.4, 0.3, 0.0, 1.0]  # Left shoulder
    kp[:, 1, :] = [0.6, 0.3, 0.0, 1.0]  # Right shoulder
    kp[:, 4, :] = [0.4, 0.7, 0.0, 1.0]  # Left hip
    kp[:, 5, :] = [0.6, 0.7, 0.0, 1.0]  # Right hip

    # Set right hand (indices 27-47) moving from frame 5 to 15
    for t in range(5, 16):
        kp[t, 27:48, 0] = 0.55
        kp[t, 27:48, 1] = 0.40 + (t - 5) * 0.02  # elevated above hip (0.7)
        kp[t, 27:48, 2] = 0.0
        kp[t, 27:48, 3] = 1.0

    features = KinematicFeatureExtractor.extract_features(kp, fps=30.0, smoothing_window=1)
    assert features["hands_present"].shape == (T,)
    assert not features["hands_present"][0]
    assert features["hands_present"][8]
    assert features["in_signing_space"][8]
    assert features["wrist_velocity"][6] > 0.0


def test_segment_extractor_validation():
    """Verify validation gating rejecting too-short or empty segments."""
    cfg = SegmentationConfig(min_segment_frames=6, min_hand_presence_ratio=0.3)
    extractor = SegmentExtractor(cfg)

    # Synthetic keypoints
    kp = np.zeros((30, 94, 4), dtype=np.float32)
    # Give hand presence to frames 10-25
    kp[10:26, 27:48, :3] = 0.5
    kp[10:26, :, 3] = 1.0

    raw_boundaries = [
        (0, 3),    # Too short (4 frames < 6)
        (10, 22),  # Valid (13 frames, hands present)
    ]
    extracted = extractor.extract_segments(kp, raw_boundaries, fps=30.0)
    assert len(extracted) == 2
    assert not extracted[0]["metadata"].is_valid
    assert extracted[1]["metadata"].is_valid
    assert extracted[1]["metadata"].segment_id == "seg_002"
    assert extracted[1]["landmarks"].shape == (13, 94, 4)


def test_evaluator_metrics():
    """Verify evaluation precision, recall, and F1 calculation against known pairs."""
    evaluator = SegmentationEvaluator(time_tolerance_seconds=0.20, iou_threshold=0.30)

    gt_segments = [
        {"start_time": 1.0, "end_time": 2.0, "label": "HELLO"},
        {"start_time": 3.0, "end_time": 4.0, "label": "WORLD"},
    ]

    pred_segments = [
        {"start_timestamp": 1.05, "end_timestamp": 1.95},  # Perfect match (tIoU ~ 0.9)
        {"start_timestamp": 3.10, "end_timestamp": 3.90},  # Perfect match (tIoU ~ 0.8)
    ]

    metrics = evaluator.evaluate(
        predicted_segments=pred_segments,
        ground_truth_segments=gt_segments,
        total_duration_seconds=5.0,
        processing_time_seconds=0.05,
    )

    assert metrics["boundary_metrics"]["precision"] == 1.0
    assert metrics["boundary_metrics"]["recall"] == 1.0
    assert metrics["boundary_metrics"]["f1_score"] == 1.0
    assert metrics["segment_metrics"]["precision"] == 1.0
    assert metrics["segment_metrics"]["recall"] == 1.0
    assert metrics["rates"]["over_segmentation_rate"] == 0.0


def test_real_keypoints_segmentation():
    """Run segmenter on real pre-extracted keypoints from workspace."""
    kp_path = PROJECT_ROOT / "research" / "video_pipeline" / "results_part2_2" / "vidssavecom-president-prime-minister-chief-minister-indian-sign-language-i_KWDwb1ih_keypoints.npy"
    if not kp_path.exists():
        pytest.skip("Test video keypoints not found.")

    keypoints = np.load(str(kp_path))
    segmenter = ContinuousSignSegmenter(SegmentationConfig())
    res = segmenter.segment(keypoints, fps=30.0, approach="combined")

    assert "raw_segments" in res
    assert len(res["frame_states"]) == len(keypoints)
    assert len(res["raw_segments"]) >= 1
