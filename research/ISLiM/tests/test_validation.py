"""
Unit tests for ISLiM landmark sequence validation.
"""

import sys
import unittest
from pathlib import Path
import numpy as np

# Ensure research/ISLiM is on sys.path
TEST_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TEST_DIR.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from preprocessing.validation import (
    PreprocessingValidationError,
    validate_sequence,
    assert_valid_sequence,
)


class TestValidation(unittest.TestCase):
    def test_valid_sequence(self):
        seq = np.random.uniform(0.0, 1.0, size=(50, 94, 4)).astype(np.float32)
        is_valid, err = validate_sequence(seq)
        self.assertTrue(is_valid)
        self.assertIsNone(err)

        out = assert_valid_sequence(seq)
        self.assertEqual(out.shape, (50, 94, 4))
        self.assertEqual(out.dtype, np.float32)

    def test_valid_batched_sequence(self):
        batch = np.random.uniform(0.0, 1.0, size=(2, 60, 94, 4)).astype(np.float32)
        is_valid, err = validate_sequence(batch)
        self.assertTrue(is_valid)
        self.assertIsNone(err)

    def test_empty_sequence(self):
        empty = np.zeros((0, 94, 4), dtype=np.float32)
        is_valid, err = validate_sequence(empty)
        self.assertFalse(is_valid)
        self.assertIn("empty", err)

        with self.assertRaises(PreprocessingValidationError) as ctx:
            assert_valid_sequence(empty)
        self.assertIn("empty", str(ctx.exception))

    def test_invalid_dimensions(self):
        # 1D array
        arr_1d = np.zeros(94, dtype=np.float32)
        is_valid, err = validate_sequence(arr_1d)
        self.assertFalse(is_valid)

        with self.assertRaises(PreprocessingValidationError):
            assert_valid_sequence(arr_1d)

        # 5D array
        arr_5d = np.zeros((1, 2, 3, 94, 4), dtype=np.float32)
        is_valid, err = validate_sequence(arr_5d)
        self.assertFalse(is_valid)

    def test_invalid_landmark_count(self):
        # 75 landmarks instead of 94
        bad_k = np.zeros((20, 75, 4), dtype=np.float32)
        is_valid, err = validate_sequence(bad_k)
        self.assertFalse(is_valid)
        self.assertIn("94 landmarks", err)

        with self.assertRaises(PreprocessingValidationError) as ctx:
            assert_valid_sequence(bad_k)
        self.assertIn("94 landmarks", str(ctx.exception))

    def test_invalid_channels(self):
        # 3 channels (x, y, z) missing visibility
        bad_c = np.zeros((20, 94, 3), dtype=np.float32)
        is_valid, err = validate_sequence(bad_c)
        self.assertFalse(is_valid)
        self.assertIn("4 channels", err)

        with self.assertRaises(PreprocessingValidationError) as ctx:
            assert_valid_sequence(bad_c)
        self.assertIn("4 channels", str(ctx.exception))

    def test_nan_rejection(self):
        seq = np.random.uniform(0.0, 1.0, size=(10, 94, 4)).astype(np.float32)
        seq[3, 12, 0] = np.nan
        is_valid, err = validate_sequence(seq)
        self.assertFalse(is_valid)
        self.assertIn("NaNs", err)

        with self.assertRaises(PreprocessingValidationError) as ctx:
            assert_valid_sequence(seq)
        self.assertIn("NaNs", str(ctx.exception))

    def test_inf_rejection(self):
        seq = np.random.uniform(0.0, 1.0, size=(10, 94, 4)).astype(np.float32)
        seq[5, 40, 1] = np.inf
        is_valid, err = validate_sequence(seq)
        self.assertFalse(is_valid)
        self.assertIn("Infs", err)

        with self.assertRaises(PreprocessingValidationError) as ctx:
            assert_valid_sequence(seq)
        self.assertIn("Infs", str(ctx.exception))

    def test_visibility_bounds(self):
        seq = np.random.uniform(0.0, 1.0, size=(10, 94, 4)).astype(np.float32)
        # Negative visibility
        seq[2, 5, 3] = -0.5
        is_valid, err = validate_sequence(seq)
        self.assertFalse(is_valid)
        self.assertIn("Visibility", err)

        with self.assertRaises(PreprocessingValidationError) as ctx:
            assert_valid_sequence(seq)
        self.assertIn("Visibility", str(ctx.exception))

        # Visibility > 1.0
        seq[2, 5, 3] = 2.5
        is_valid, err = validate_sequence(seq)
        self.assertFalse(is_valid)


if __name__ == "__main__":
    unittest.main()
