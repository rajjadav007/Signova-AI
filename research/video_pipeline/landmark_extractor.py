"""
MediaPipe Holistic Landmark Extractor for extracting the 94 ISLiM keypoints per frame.
Reuses the verified Phase 1 MediaPipe Tasks HolisticLandmarker API and ordering.
"""

from pathlib import Path
from typing import Any, Dict, Optional, Tuple, Union
import numpy as np

import mediapipe as mp
from mediapipe.tasks.python import vision
from mediapipe.tasks.python.core.base_options import BaseOptions

from .config import (
    DEFAULT_MODEL_ASSET_PATH,
    FACE_INDICES,
    HAND_LANDMARK_COUNT,
    KEYPOINT_COORDS,
    NUM_KEYPOINTS,
    POSE_INDICES,
)
from .exceptions import LandmarkExtractionError, ModelAssetNotFoundError


class MediaPipeLandmarkExtractor:
    """
    Extracts 94 3D keypoints + visibility (94, 4) from RGB image frames
    using MediaPipe HolisticLandmarker.
    """

    def __init__(
        self,
        model_asset_path: Optional[Union[str, Path]] = None,
        min_face_detection_confidence: float = 0.5,
        min_pose_detection_confidence: float = 0.5,
        min_hand_landmarks_confidence: float = 0.5,
    ):
        self._landmarker: Optional[vision.HolisticLandmarker] = None
        self.model_asset_path = Path(model_asset_path or DEFAULT_MODEL_ASSET_PATH).resolve()
        if not self.model_asset_path.exists():
            raise ModelAssetNotFoundError(
                f"MediaPipe model asset not found at: {self.model_asset_path}"
            )

        self.min_face_detection_confidence = min_face_detection_confidence
        self.min_pose_detection_confidence = min_pose_detection_confidence
        self.min_hand_landmarks_confidence = min_hand_landmarks_confidence

        try:
            options = vision.HolisticLandmarkerOptions(
                base_options=BaseOptions(model_asset_path=str(self.model_asset_path)),
                running_mode=vision.RunningMode.IMAGE,
                min_face_detection_confidence=self.min_face_detection_confidence,
                min_pose_detection_confidence=self.min_pose_detection_confidence,
                min_hand_landmarks_confidence=self.min_hand_landmarks_confidence,
            )
            self._landmarker: Optional[vision.HolisticLandmarker] = (
                vision.HolisticLandmarker.create_from_options(options)
            )
        except Exception as e:
            raise LandmarkExtractionError(f"Failed to initialize MediaPipe HolisticLandmarker: {e}") from e

    def extract_frame(self, rgb_frame: np.ndarray) -> Tuple[np.ndarray, Dict[str, bool]]:
        """
        Extract 94 landmarks from a single RGB uint8 image.

        Returns:
            keypoints: np.ndarray of shape (94, 4) with dtype float32 [x, y, z, visibility]
            detections: Dict[str, bool] indicating which subsystems detected landmarks
        """
        if self._landmarker is None:
            raise LandmarkExtractionError("MediaPipe landmarker is closed or not initialized.")

        if not isinstance(rgb_frame, np.ndarray) or rgb_frame.ndim != 3 or rgb_frame.shape[2] != 3:
            raise LandmarkExtractionError(
                f"Expected RGB image of shape (H, W, 3), got {getattr(rgb_frame, 'shape', type(rgb_frame))}"
            )

        # Preallocate (94, 4) zeros array
        kp = np.zeros((NUM_KEYPOINTS, KEYPOINT_COORDS), dtype=np.float32)

        detections = {
            "pose": False,
            "left_hand": False,
            "right_hand": False,
            "face": False,
        }

        try:
            mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)
            res = self._landmarker.detect(mp_image)
        except Exception as e:
            raise LandmarkExtractionError(f"Error during frame landmark detection: {e}") from e

        # 1. Pose landmarks: indices 0-5 (POSE_INDICES: 11, 12, 13, 14, 23, 24)
        if res.pose_landmarks and len(res.pose_landmarks) > 0:
            detections["pose"] = True
            for i, idx in enumerate(POSE_INDICES):
                if idx < len(res.pose_landmarks):
                    lm = res.pose_landmarks[idx]
                    vis = getattr(lm, "visibility", 1.0)
                    if vis is None:
                        vis = 1.0
                    kp[i] = [lm.x, lm.y, lm.z, vis]

        # 2. Left Hand landmarks: indices 6-26 (21 landmarks)
        if res.left_hand_landmarks and len(res.left_hand_landmarks) > 0:
            detections["left_hand"] = True
            for i in range(min(HAND_LANDMARK_COUNT, len(res.left_hand_landmarks))):
                lm = res.left_hand_landmarks[i]
                kp[6 + i] = [lm.x, lm.y, lm.z, 1.0]

        # 3. Right Hand landmarks: indices 27-47 (21 landmarks)
        if res.right_hand_landmarks and len(res.right_hand_landmarks) > 0:
            detections["right_hand"] = True
            for i in range(min(HAND_LANDMARK_COUNT, len(res.right_hand_landmarks))):
                lm = res.right_hand_landmarks[i]
                kp[27 + i] = [lm.x, lm.y, lm.z, 1.0]

        # 4. Face mesh: indices 48-93 (46 landmarks: Lips 20, Eyes 16, Eyebrows 10)
        if res.face_landmarks and len(res.face_landmarks) > 0:
            detections["face"] = True
            for i, idx in enumerate(FACE_INDICES):
                if idx < len(res.face_landmarks):
                    lm = res.face_landmarks[idx]
                    vis = 1.0 if lm.z > -0.5 else 0.5
                    kp[48 + i] = [lm.x, lm.y, lm.z, vis]

        return kp, detections

    def close(self) -> None:
        """Release MediaPipe resources."""
        if hasattr(self, "_landmarker") and self._landmarker is not None:
            self._landmarker.close()
            self._landmarker = None

    def __enter__(self) -> "MediaPipeLandmarkExtractor":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.close()

    def __del__(self) -> None:
        self.close()
