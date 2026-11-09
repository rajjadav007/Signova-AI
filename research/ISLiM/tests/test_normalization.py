"""
Unit tests for ISLiM spatial coordinate min-max normalization.
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

from preprocessing.normalization import normalize_coordinates, EPSILON


class TestNormalization(unittest.TestCase):
    def test_standard_normalization(self):
        seq = np.zeros((10, 94, 4), dtype=np.float32)
        seq[:, :, 0] = np.linspace(-5.0, 15.0, 10)[:, None]
        seq[:, :, 1] = np.linspace(10.0, 20.0, 10)[:, None]
        seq[:, :, 2] = np.linspace(0.0, 100.0, 10)[:, None]
        seq[:, :, 3] = 0.75

        out = normalize_coordinates(seq, copy=True)

        self.assertGreaterEqual(float(out[:, :, :3].min()), 0.0)
        self.assertLessEqual(float(out[:, :, :3].max()), 1.0)

        np.testing.assert_allclose(out[:, :, 0].min(), 0.0, atol=1e-6)
        np.testing.assert_allclose(out[:, :, 0].max(), 1.0, atol=1e-6)
        np.testing.assert_allclose(out[:, :, 1].min(), 0.0, atol=1e-6)
        np.testing.assert_allclose(out[:, :, 1].max(), 1.0, atol=1e-6)
        np.testing.assert_allclose(out[:, :, 2].min(), 0.0, atol=1e-6)
        np.testing.assert_allclose(out[:, :, 2].max(), 1.0, atol=1e-6)

        np.testing.assert_allclose(out[:, :, 3], 0.75)

    def test_constant_coordinates(self):
        seq = np.zeros((10, 94, 4), dtype=np.float32)
        seq[:, :, 0] = 42.0
        seq[:, :, 1] = np.linspace(0.0, 10.0, 10)[:, None]
        seq[:, :, 2] = 0.0
        seq[:, :, 3] = 1.0

        out = normalize_coordinates(seq, copy=True)

        np.testing.assert_allclose(out[:, :, 0], 0.0)
        np.testing.assert_allclose(out[:, :, 2], 0.0)
        np.testing.assert_allclose(out[:, :, 1].min(), 0.0)
        np.testing.assert_allclose(out[:, :, 1].max(), 1.0)

    def test_epsilon_threshold(self):
        seq = np.zeros((10, 94, 4), dtype=np.float32)
        seq[0, :, 0] = 0.0
        seq[1, :, 0] = 1e-9
        seq[:, :, 3] = 1.0

        out = normalize_coordinates(seq, copy=True)
        np.testing.assert_allclose(out[0, :, 0], 0.0)
        np.testing.assert_allclose(out[1, :, 0], 1e-9)

    def test_copy_semantics(self):
        seq = np.zeros((10, 94, 4), dtype=np.float32)
        seq[:, :, 0] = 10.0
        out = normalize_coordinates(seq, copy=True)
        self.assertEqual(float(seq[:, :, 0].max()), 10.0)
        self.assertEqual(float(out[:, :, 0].max()), 0.0)

    def test_batched_normalization(self):
        batch = np.zeros((2, 10, 94, 4), dtype=np.float32)
        batch[0, :, :, 0] = np.linspace(0.0, 10.0, 10)[:, None]
        batch[1, :, :, 0] = np.linspace(100.0, 200.0, 10)[:, None]

        out = normalize_coordinates(batch, copy=True)
        self.assertEqual(out.shape, (2, 10, 94, 4))

        np.testing.assert_allclose(out[0, :, :, 0].min(), 0.0)
        np.testing.assert_allclose(out[0, :, :, 0].max(), 1.0)
        np.testing.assert_allclose(out[1, :, :, 0].min(), 0.0)
        np.testing.assert_allclose(out[1, :, :, 0].max(), 1.0)


if __name__ == "__main__":
    unittest.main()
