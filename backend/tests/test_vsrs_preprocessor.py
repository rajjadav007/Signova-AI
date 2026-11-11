"""
Unit tests for VSRS Hand Landmark Preprocessor (Signova AI - Step 3).
Verifies wrist-centered translation, max-radius scale normalization,
126-D feature ordering (Right 0..62, Left 63..125), zero-padding,
invalid detection state, mirroring behavior, and model prediction compatibility.
"""

from pathlib import Path
from types import SimpleNamespace
import numpy as np
import pytest

from backend.app.ml.preprocessing.vsrs_preprocessor import (
    COORDS_PER_LANDMARK,
    HAND_FEATURE_DIM,
    LANDMARKS_PER_HAND,
    TOTAL_FEATURE_DIM,
    VSRSPreprocessResult,
    VSRSPreprocessor,
)


def create_mock_landmark(x: float, y: float, z: float) -> SimpleNamespace:
    return SimpleNamespace(x=x, y=y, z=z)


def create_mock_hand(wrist_x: float = 0.5, wrist_y: float = 0.5, wrist_z: float = 0.0) -> list:
    """Creates 21 synthetic hand landmarks anchored at wrist."""
    landmarks = []
    # Landmark 0: Wrist
    landmarks.append(create_mock_landmark(wrist_x, wrist_y, wrist_z))
    # Landmarks 1..20: Radiating out along fingers
    for i in range(1, LANDMARKS_PER_HAND):
        angle = (i / 20.0) * np.pi
        r = 0.1 * (1 + (i % 4))
        lx = wrist_x + r * np.cos(angle)
        ly = wrist_y + r * np.sin(angle)
        lz = wrist_z + 0.05 * (i % 3)
        landmarks.append(create_mock_landmark(lx, ly, lz))
    return landmarks


def create_mock_handedness(label: str) -> list:
    return [SimpleNamespace(category_name=label, display_name=label)]


class TestVSRSPreprocessor:
    """Test suite for VSRSPreprocessor."""

    @pytest.fixture
    def preprocessor(self) -> VSRSPreprocessor:
        return VSRSPreprocessor(mirror=False)

    def test_both_hands_detected(self, preprocessor: VSRSPreprocessor):
        """Test with both right and left hands detected."""
        right_hand = create_mock_hand(0.3, 0.4, 0.1)
        left_hand = create_mock_hand(0.7, 0.4, -0.1)

        result = preprocessor.process_raw(
            hand_landmarks_list=[right_hand, left_hand],
            handedness_list=[create_mock_handedness("Right"), create_mock_handedness("Left")],
        )

        assert isinstance(result, VSRSPreprocessResult)
        assert result.is_valid is True
        assert bool(result) is True
        assert result.features is not None
        assert result.features.shape == (TOTAL_FEATURE_DIM,)
        assert result.features.dtype == np.float32

        # Check right hand slot (0..62) is populated and non-zero
        right_slice = result.features[:HAND_FEATURE_DIM]
        assert np.any(right_slice != 0.0)

        # Check left hand slot (63..125) is populated and non-zero
        left_slice = result.features[HAND_FEATURE_DIM:]
        assert np.any(left_slice != 0.0)

        # Verify no NaN or infinity
        assert np.all(np.isfinite(result.features))

    def test_only_right_hand_detected(self, preprocessor: VSRSPreprocessor):
        """Test with only right hand detected; left hand slot must be zero-padded."""
        right_hand = create_mock_hand(0.5, 0.5, 0.0)

        result = preprocessor.process_raw(
            hand_landmarks_list=[right_hand],
            handedness_list=[create_mock_handedness("Right")],
        )

        assert result.is_valid is True
        assert result.features is not None
        assert result.features.shape == (TOTAL_FEATURE_DIM,)

        # Right hand populated
        right_slice = result.features[:HAND_FEATURE_DIM]
        assert np.any(right_slice != 0.0)

        # Left hand strictly zero-padded (63 zeros)
        left_slice = result.features[HAND_FEATURE_DIM:]
        assert len(left_slice) == 63
        assert np.all(left_slice == 0.0)
        assert np.all(np.isfinite(result.features))

    def test_only_left_hand_detected(self, preprocessor: VSRSPreprocessor):
        """Test with only left hand detected; right hand slot must be zero-padded."""
        left_hand = create_mock_hand(0.5, 0.5, 0.0)

        result = preprocessor.process_raw(
            hand_landmarks_list=[left_hand],
            handedness_list=[create_mock_handedness("Left")],
        )

        assert result.is_valid is True
        assert result.features is not None
        assert result.features.shape == (TOTAL_FEATURE_DIM,)

        # Right hand strictly zero-padded (63 zeros)
        right_slice = result.features[:HAND_FEATURE_DIM]
        assert len(right_slice) == 63
        assert np.all(right_slice == 0.0)

        # Left hand populated
        left_slice = result.features[HAND_FEATURE_DIM:]
        assert np.any(left_slice != 0.0)
        assert np.all(np.isfinite(result.features))

    def test_no_hands_detected(self, preprocessor: VSRSPreprocessor):
        """Test when no hands are detected: must return explicit invalid result."""
        # Empty list
        res_empty = preprocessor.process_raw([], [])
        assert res_empty.is_valid is False
        assert res_empty.features is None
        assert bool(res_empty) is False

        # None input
        res_none = preprocessor.process(None)
        assert res_none.is_valid is False
        assert res_none.features is None

        # Dict with empty landmarks
        res_dict_empty = preprocessor.process({"hand_landmarks": [], "handedness": []})
        assert res_dict_empty.is_valid is False
        assert res_dict_empty.features is None

        # NamedTuple unpacking works safely
        features, is_valid = preprocessor.process(None)
        assert features is None
        assert is_valid is False

    def test_wrist_centered_translation(self, preprocessor: VSRSPreprocessor):
        """Verify wrist (landmark 0) coordinate is exactly [0.0, 0.0, 0.0]."""
        wrist_pos = (123.45, 678.90, -42.0)
        hand = create_mock_hand(*wrist_pos)

        coords_21x3 = np.array([[lm.x, lm.y, lm.z] for lm in hand], dtype=np.float32)
        norm_63 = preprocessor.normalize_hand_landmarks(coords_21x3)

        # Landmark 0 corresponds to indices 0, 1, 2
        wrist_norm = norm_63[0:3]
        np.testing.assert_allclose(wrist_norm, [0.0, 0.0, 0.0], atol=1e-7)

    def test_max_radius_scale_normalization(self, preprocessor: VSRSPreprocessor):
        """Verify max Euclidean distance from origin across all 21 keypoints is exactly 1.0."""
        hand = create_mock_hand(0.2, 0.3, 0.1)
        coords_21x3 = np.array([[lm.x, lm.y, lm.z] for lm in hand], dtype=np.float32)

        norm_63 = preprocessor.normalize_hand_landmarks(coords_21x3)
        points = norm_63.reshape(21, 3)

        distances = np.linalg.norm(points, axis=1)
        assert np.isclose(np.max(distances), 1.0, atol=1e-6)
        # All points are within unit ball
        assert np.all(distances <= 1.0 + 1e-6)

    def test_camera_mirroring_behavior(self):
        """Verify mirror=True correctly flips handedness slots."""
        preprocessor_normal = VSRSPreprocessor(mirror=False)
        preprocessor_mirrored = VSRSPreprocessor(mirror=True)

        hand = create_mock_hand(0.5, 0.5, 0.0)

        # In unmirrored feed: Left hand goes to left slot (63..125)
        res_norm = preprocessor_normal.process_raw([hand], [create_mock_handedness("Left")])
        assert np.all(res_norm.features[:63] == 0.0)
        assert np.any(res_norm.features[63:] != 0.0)

        # In mirrored feed: Left hand flipped to Right slot (0..62)
        res_mirrored = preprocessor_mirrored.process_raw([hand], [create_mock_handedness("Left")])
        assert np.any(res_mirrored.features[:63] != 0.0)
        assert np.all(res_mirrored.features[63:] == 0.0)

    def test_degenerate_zero_radius_hand(self, preprocessor: VSRSPreprocessor):
        """Verify hand with all identical coordinates (radius=0) does not produce NaN/Inf."""
        zeros_hand = np.zeros((21, 3), dtype=np.float32)
        norm_63 = preprocessor.normalize_hand_landmarks(zeros_hand)
        assert norm_63.shape == (63,)
        assert np.all(norm_63 == 0.0)
        assert np.all(np.isfinite(norm_63))

    def test_mediapipe_result_object_input(self, preprocessor: VSRSPreprocessor):
        """Verify MediaPipe HandLandmarkerResult object structure compatibility."""
        mock_result = SimpleNamespace(
            hand_landmarks=[create_mock_hand(0.4, 0.5, 0.0)],
            handedness=[create_mock_handedness("Right")],
        )
        res = preprocessor.process(mock_result)
        assert res.is_valid is True
        assert res.features.shape == (TOTAL_FEATURE_DIM,)
        assert np.all(np.isfinite(res.features))

    def test_compatibility_with_downloaded_vsrs_model(self, preprocessor: VSRSPreprocessor):
        """Verify preprocessed 126-D output runs through actual downloaded VSRS MLP model."""
        model_path = Path("models/checkpoints/vsrs/model.joblib")
        if not model_path.exists():
            pytest.skip("VSRS model.joblib not present")

        from scripts.download_and_verify_vsrs import load_vsrs_artifact
        artifact = load_vsrs_artifact(model_path)
        model = artifact["model"]
        scaler = artifact["scaler"]
        classes = artifact["classes"]

        # Generate preprocessed features from mock hands
        right_hand = create_mock_hand(0.3, 0.4, 0.0)
        left_hand = create_mock_hand(0.7, 0.4, 0.0)
        res = preprocessor.process_raw(
            hand_landmarks_list=[right_hand, left_hand],
            handedness_list=[create_mock_handedness("Right"), create_mock_handedness("Left")],
        )

        assert res.is_valid is True
        features_2d = res.features.reshape(1, -1)

        # Scale features and infer
        scaled = scaler.transform(features_2d)
        pred = model.predict(scaled)
        probs = model.predict_proba(scaled)

        assert probs.shape == (1, 11)
        assert np.isclose(np.sum(probs), 1.0, atol=1e-5)
        pred_label = classes[pred[0]] if isinstance(pred[0], (int, np.integer)) else pred[0]
        assert pred_label in classes
