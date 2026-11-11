"""
MediaPipe Holistic Landmark Extractor for extracting 94 ISL keypoints per frame.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union
import numpy as np

try:
    import mediapipe as mp
    from mediapipe.tasks.python import vision
    from mediapipe.tasks.python.core.base_options import BaseOptions
    MEDIAPIPE_AVAILABLE = True
except ImportError:
    MEDIAPIPE_AVAILABLE = False

from ai.config.settings import (
    DEFAULT_MEDIAPIPE_TASK_PATH,
    FACE_INDICES,
    HAND_LANDMARK_COUNT,
    NUM_KEYPOINTS,
    POSE_INDICES,
)


class MediaPipeLandmarkExtractor:
    """Extracts 94 3D keypoints + visibility (94, 4) from RGB image frames."""

    def __init__(
        self,
        model_asset_path: Optional[Union[str, Path]] = None,
        min_face_detection_confidence: float = 0.5,
        min_pose_detection_confidence: float = 0.5,
        min_hand_landmarks_confidence: float = 0.5,
    ) -> None:
        if not MEDIAPIPE_AVAILABLE:
            raise ImportError("mediapipe package is not installed.")

        self.model_asset_path = Path(model_asset_path or DEFAULT_MEDIAPIPE_TASK_PATH).resolve()
        if not self.model_asset_path.exists():
            raise FileNotFoundError(f"MediaPipe model asset not found at: {self.model_asset_path}")

        options = vision.HolisticLandmarkerOptions(
            base_options=BaseOptions(model_asset_path=str(self.model_asset_path)),
            running_mode=vision.RunningMode.IMAGE,
            min_face_detection_confidence=min_face_detection_confidence,
            min_pose_detection_confidence=min_pose_detection_confidence,
            min_hand_landmarks_confidence=min_hand_landmarks_confidence,
        )
        self._landmarker = vision.HolisticLandmarker.create_from_options(options)

    def extract_frame(self, rgb_frame: np.ndarray) -> Tuple[np.ndarray, Dict[str, bool]]:
        """
        Extract 94 landmarks from a single RGB uint8 image.
        Returns:
            keypoints: (94, 4) float32 array [x, y, z, visibility]
            detections: Dict indicating detected components
        """
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
        result = self._landmarker.detect(mp_image)

        keypoints = np.zeros((NUM_KEYPOINTS, 4), dtype=np.float32)
        detections = {"pose": False, "left_hand": False, "right_hand": False, "face": False}

        # 1. Pose landmarks (6 keypoints)
        if result.pose_landmarks and len(result.pose_landmarks) > 0:
            pose_lms = result.pose_landmarks[0]
            detections["pose"] = True
            for out_idx, p_idx in enumerate(POSE_INDICES):
                if p_idx < len(pose_lms):
                    lm = pose_lms[p_idx]
                    vis = getattr(lm, "visibility", 1.0)
                    keypoints[out_idx] = [lm.x, lm.y, lm.z, vis]

        # 2. Left hand (21 keypoints, slots 6..26)
        if result.left_hand_landmarks and len(result.left_hand_landmarks) > 0:
            detections["left_hand"] = True
            for i, lm in enumerate(result.left_hand_landmarks[0][:HAND_LANDMARK_COUNT]):
                keypoints[6 + i] = [lm.x, lm.y, lm.z, 1.0]

        # 3. Right hand (21 keypoints, slots 27..47)
        if result.right_hand_landmarks and len(result.right_hand_landmarks) > 0:
            detections["right_hand"] = True
            for i, lm in enumerate(result.right_hand_landmarks[0][:HAND_LANDMARK_COUNT]):
                keypoints[27 + i] = [lm.x, lm.y, lm.z, 1.0]

        # 4. Face mesh (46 keypoints, slots 48..93)
        if result.face_landmarks and len(result.face_landmarks) > 0:
            detections["face"] = True
            face_lms = result.face_landmarks[0]
            for out_offset, f_idx in enumerate(FACE_INDICES):
                if f_idx < len(face_lms):
                    lm = face_lms[f_idx]
                    keypoints[48 + out_offset] = [lm.x, lm.y, lm.z, 1.0]

        return keypoints, detections

    def close(self) -> None:
        if hasattr(self, "_landmarker") and self._landmarker is not None:
            self._landmarker.close()
            self._landmarker = None
