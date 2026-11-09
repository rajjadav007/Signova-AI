"""
Configuration and landmark index specifications for the Signova AI video pipeline.
Reuses the exact 94-landmark ordering verified in Phase 1 ISLiM preprocessing.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Set

# Root directories
PIPELINE_DIR = Path(__file__).resolve().parent
PROJECT_ROOT = PIPELINE_DIR.parent.parent

# Video Formats
SUPPORTED_FORMATS: Set[str] = {".mp4", ".avi", ".mov", ".mkv"}

# Landmark Dimensions
NUM_KEYPOINTS: int = 94
KEYPOINT_COORDS: int = 4  # [x, y, z, visibility]

# Landmark Group Indices (MediaPipe Holistic Mapping)
# 1. Pose: Upper torso (Left/Right Shoulder, Elbow, Hip)
POSE_INDICES: List[int] = [11, 12, 13, 14, 23, 24]
POSE_COUNT: int = len(POSE_INDICES)  # 6

# 2. Hands: 21 landmarks per hand (Wrist + 4 joints * 5 fingers)
HAND_LANDMARK_COUNT: int = 21

# 3. Face Mesh Subsets: Lips (20), Eyes (16), Eyebrows (10)
FACE_LIPS: List[int] = [
    61, 146, 91, 181, 84, 17, 314, 405, 321, 375,
    291, 409, 270, 95, 88, 178, 87, 14, 78, 308,
]
FACE_EYES: List[int] = [
    33, 133, 160, 158, 153, 144, 145, 246,
    362, 263, 387, 385, 380, 373, 374, 249,
]
FACE_EYEBROWS: List[int] = [
    107, 66, 105, 63, 70,
    336, 296, 334, 293, 300,
]
FACE_INDICES: List[int] = FACE_LIPS + FACE_EYES + FACE_EYEBROWS
FACE_COUNT: int = len(FACE_INDICES)  # 46

# Group Slices in the final (94, 4) landmark array
GROUP_SLICES: Dict[str, slice] = {
    "pose": slice(0, 6),
    "left_hand": slice(6, 27),
    "right_hand": slice(27, 48),
    "lips": slice(48, 68),
    "eyes": slice(68, 84),
    "eyebrows": slice(84, 94),
}

# Default Paths
DEFAULT_MODEL_ASSET_PATH: Path = (
    Path(os.environ["MEDIAPIPE_MODEL_PATH"]).resolve()
    if "MEDIAPIPE_MODEL_PATH" in os.environ
    else PROJECT_ROOT / "research" / "ISLiM" / "assets" / "holistic_landmarker.task"
)

DEFAULT_RESULTS_DIR: Path = PIPELINE_DIR / "results"


@dataclass
class VideoPipelineConfig:
    """Configuration container for video reading and landmark extraction."""
    model_asset_path: Path = DEFAULT_MODEL_ASSET_PATH
    results_dir: Path = DEFAULT_RESULTS_DIR
    min_face_detection_confidence: float = 0.5
    min_pose_detection_confidence: float = 0.5
    min_hand_landmarks_confidence: float = 0.5

    def __post_init__(self):
        self.model_asset_path = Path(self.model_asset_path).resolve()
        self.results_dir = Path(self.results_dir).resolve()
