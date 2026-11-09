"""
Unit tests for MediaPipeLandmarkExtractor.
Tests landmark ordering, output shapes, dtype, missing landmark fallback, and cleanup.
"""

from pathlib import Path
import tempfile
import unittest
import numpy as np

from research.video_pipeline.config import (
    DEFAULT_MODEL_ASSET_PATH,
    FACE_EYEBROWS,
    FACE_EYES,
    FACE_INDICES,
    FACE_LIPS,
    GROUP_SLICES,
    HAND_LANDMARK_COUNT,
    KEYPOINT_COORDS,
    NUM_KEYPOINTS,
    POSE_INDICES,
)
from research.video_pipeline.exceptions import (
    LandmarkExtractionError,
    ModelAssetNotFoundError,
)
from research.video_pipeline.landmark_extractor import MediaPipeLandmarkExtractor


class TestLandmarkExtractor(unittest.TestCase):
    def test_landmark_definitions_and_ordering(self):
        """Verify landmark indices and slice layout strictly match ISLiM specification."""
        self.assertEqual(len(POSE_INDICES), 6)
        self.assertEqual(POSE_INDICES, [11, 12, 13, 14, 23, 24])

        self.assertEqual(HAND_LANDMARK_COUNT, 21)
        self.assertEqual(len(FACE_LIPS), 20)
        self.assertEqual(len(FACE_EYES), 16)
        self.assertEqual(len(FACE_EYEBROWS), 10)
        self.assertEqual(len(FACE_INDICES), 46)

        # Verify slices
        self.assertEqual(GROUP_SLICES["pose"], slice(0, 6))
        self.assertEqual(GROUP_SLICES["left_hand"], slice(6, 27))
        self.assertEqual(GROUP_SLICES["right_hand"], slice(27, 48))
        self.assertEqual(GROUP_SLICES["lips"], slice(48, 68))
        self.assertEqual(GROUP_SLICES["eyes"], slice(68, 84))
        self.assertEqual(GROUP_SLICES["eyebrows"], slice(84, 94))

        total_landmarks = (
            (6 - 0) + (27 - 6) + (48 - 27) + (68 - 48) + (84 - 68) + (94 - 84)
        )
        self.assertEqual(total_landmarks, NUM_KEYPOINTS)
        self.assertEqual(NUM_KEYPOINTS, 94)
        self.assertEqual(KEYPOINT_COORDS, 4)

    def test_landmark_extractor_missing_asset(self):
        """Verify ModelAssetNotFoundError when asset file is missing."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            non_existent = Path(tmp_dir) / "missing_model.task"
            with self.assertRaises(ModelAssetNotFoundError) as ctx:
                MediaPipeLandmarkExtractor(model_asset_path=non_existent)
            self.assertIn("not found", str(ctx.exception).lower())

    def test_landmark_extractor_blank_frame(self):
        """Verify extraction on a blank frame produces (94, 4) zeros with float32 dtype."""
        self.assertTrue(DEFAULT_MODEL_ASSET_PATH.exists(), f"Asset not found: {DEFAULT_MODEL_ASSET_PATH}")

        with MediaPipeLandmarkExtractor() as extractor:
            blank = np.zeros((240, 240, 3), dtype=np.uint8)
            kp, detections = extractor.extract_frame(blank)

            self.assertIsInstance(kp, np.ndarray)
            self.assertEqual(kp.shape, (94, 4))
            self.assertEqual(kp.dtype, np.float32)

            # In a blank frame, no person or hands are detected -> all zeros
            self.assertTrue(np.all(kp == 0.0))
            self.assertFalse(detections["pose"])
            self.assertFalse(detections["left_hand"])
            self.assertFalse(detections["right_hand"])
            self.assertFalse(detections["face"])

    def test_landmark_extractor_invalid_input(self):
        """Verify LandmarkExtractionError on invalid frame shape or type."""
        with MediaPipeLandmarkExtractor() as extractor:
            # Invalid dimension: 2D instead of 3D
            with self.assertRaises(LandmarkExtractionError):
                extractor.extract_frame(np.zeros((100, 100), dtype=np.uint8))

            # Invalid channels: 4 channels instead of 3
            with self.assertRaises(LandmarkExtractionError):
                extractor.extract_frame(np.zeros((100, 100, 4), dtype=np.uint8))

    def test_landmark_extractor_resource_cleanup(self):
        """Verify landmarker closes cleanly and rejects further extraction."""
        extractor = MediaPipeLandmarkExtractor()
        self.assertIsNotNone(extractor._landmarker)
        extractor.close()
        self.assertIsNone(extractor._landmarker)

        # Subsequent extract_frame should raise LandmarkExtractionError
        blank = np.zeros((100, 100, 3), dtype=np.uint8)
        with self.assertRaises(LandmarkExtractionError):
            extractor.extract_frame(blank)


if __name__ == "__main__":
    unittest.main()
