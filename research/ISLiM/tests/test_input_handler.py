"""
Unit tests for ISLiM Input Handler (Part 1.9).
"""

from pathlib import Path
import sys
import unittest
import tempfile
import numpy as np

TEST_DIR = Path(__file__).resolve().parent
ISLIM_DIR = TEST_DIR.parent
if str(ISLIM_DIR) not in sys.path:
    sys.path.insert(0, str(ISLIM_DIR))

from inference.input_handler import (
    validate_keypoint_array,
    load_keypoints_from_file,
    resolve_input,
)
from inference.exceptions import InvalidInputError


class TestInputHandler(unittest.TestCase):
    def test_valid_3d_keypoints(self):
        """Verify valid (T, 94, 4) array passes validation."""
        arr = np.random.rand(50, 94, 4).astype(np.float32)
        val = validate_keypoint_array(arr)
        self.assertEqual(val.shape, (50, 94, 4))
        self.assertEqual(val.dtype, np.float32)

    def test_valid_4d_keypoints(self):
        """Verify valid (B, T, 94, 4) batch passes validation."""
        arr = np.random.rand(2, 60, 94, 4).astype(np.float32)
        val = validate_keypoint_array(arr)
        self.assertEqual(val.shape, (2, 60, 94, 4))

    def test_empty_array(self):
        """Verify empty array is rejected."""
        empty = np.array([])
        with self.assertRaises(InvalidInputError) as ctx:
            validate_keypoint_array(empty)
        self.assertIn("empty", str(ctx.exception))

    def test_nan_values(self):
        """Verify NaN values are rejected."""
        arr = np.zeros((30, 94, 4), dtype=np.float32)
        arr[5, 10, 0] = np.nan
        with self.assertRaises(InvalidInputError) as ctx:
            validate_keypoint_array(arr)
        self.assertIn("NaN", str(ctx.exception))

    def test_infinite_values(self):
        """Verify infinite values are rejected."""
        arr = np.zeros((30, 94, 4), dtype=np.float32)
        arr[5, 10, 0] = np.inf
        with self.assertRaises(InvalidInputError) as ctx:
            validate_keypoint_array(arr)
        self.assertIn("infinite", str(ctx.exception))

    def test_wrong_landmarks(self):
        """Verify wrong landmark count (e.g. 75 instead of 94) is rejected."""
        arr = np.zeros((30, 75, 4), dtype=np.float32)
        with self.assertRaises(InvalidInputError) as ctx:
            validate_keypoint_array(arr)
        self.assertIn("expected 94 landmarks", str(ctx.exception))

    def test_wrong_channels(self):
        """Verify wrong channel count (e.g. 3 instead of 4) is rejected."""
        arr = np.zeros((30, 94, 3), dtype=np.float32)
        with self.assertRaises(InvalidInputError) as ctx:
            validate_keypoint_array(arr)
        self.assertIn("expected 4 channels", str(ctx.exception))

    def test_missing_file(self):
        """Verify missing file raises InvalidInputError."""
        with self.assertRaises(InvalidInputError) as ctx:
            load_keypoints_from_file("non_existent_file.npy")
        self.assertIn("not found", str(ctx.exception))

    def test_invalid_extension(self):
        """Verify non-.npy file extension is rejected."""
        with tempfile.NamedTemporaryFile(suffix=".mp4") as tmp:
            with self.assertRaises(InvalidInputError) as ctx:
                load_keypoints_from_file(tmp.name)
            self.assertIn("Only NumPy '.npy' files", str(ctx.exception))

    def test_file_loading_roundtrip(self):
        """Verify saving and loading .npy file works with security checks."""
        arr = np.random.rand(40, 94, 4).astype(np.float32)
        with tempfile.NamedTemporaryFile(suffix=".npy", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            np.save(tmp_path, arr)
            loaded = load_keypoints_from_file(tmp_path)
            self.assertEqual(loaded.shape, (40, 94, 4))
            np.testing.assert_allclose(loaded, arr, rtol=1e-5)
        finally:
            if tmp_path.exists():
                tmp_path.unlink()


if __name__ == "__main__":
    unittest.main()
