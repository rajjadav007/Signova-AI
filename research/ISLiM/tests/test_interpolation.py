"""
Unit tests for ISLiM temporal landmark interpolation.
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

from preprocessing.interpolation import interpolate_keypoints


class TestInterpolation(unittest.TestCase):
    def test_single_missing_frame(self):
        # Sequence of 10 frames, landmark 0 has gap at frame 4
        seq = np.zeros((10, 94, 4), dtype=np.float32)
        for f in range(10):
            seq[f, 0] = [float(f), float(f) * 2, float(f) * 3, 1.0]
        seq[4, 0] = [0.0, 0.0, 0.0, 0.0]  # missing frame

        out = interpolate_keypoints(seq, copy=True)

        expected_x = (seq[3, 0, 0] + seq[5, 0, 0]) / 2.0  # 4.0
        expected_y = (seq[3, 0, 1] + seq[5, 0, 1]) / 2.0  # 8.0
        expected_z = (seq[3, 0, 2] + seq[5, 0, 2]) / 2.0  # 12.0

        np.testing.assert_allclose(out[4, 0, 0], expected_x)
        np.testing.assert_allclose(out[4, 0, 1], expected_y)
        np.testing.assert_allclose(out[4, 0, 2], expected_z)
        self.assertEqual(out[4, 0, 3], 1.0)

    def test_gap_boundary_at_five_frames(self):
        # 4 missing frames: gap = 5 <= 5 -> should interpolate
        seq = np.zeros((10, 94, 4), dtype=np.float32)
        seq[0, 0] = [0.0, 0.0, 0.0, 1.0]
        seq[5, 0] = [5.0, 10.0, 15.0, 1.0]

        out = interpolate_keypoints(seq, copy=True)
        self.assertGreater(out[1, 0, 3], 0.5)
        self.assertGreater(out[4, 0, 3], 0.5)
        np.testing.assert_allclose(out[1, 0, 0], 1.0)
        np.testing.assert_allclose(out[2, 0, 0], 2.0)
        np.testing.assert_allclose(out[3, 0, 0], 3.0)
        np.testing.assert_allclose(out[4, 0, 0], 4.0)

    def test_gap_exceeding_five_frames(self):
        # 5 missing frames: gap = 6 > 5 -> should NOT interpolate, remain 0.0
        seq = np.zeros((12, 94, 4), dtype=np.float32)
        seq[0, 0] = [1.0, 1.0, 1.0, 1.0]
        seq[6, 0] = [7.0, 7.0, 7.0, 1.0]

        out = interpolate_keypoints(seq, copy=True)
        self.assertTrue((out[1:6, 0] == 0.0).all())

    def test_boundary_extrapolation(self):
        seq = np.zeros((10, 94, 4), dtype=np.float32)
        for f in range(3, 8):
            seq[f, 0] = [10.0, 20.0, 30.0, 1.0]

        out = interpolate_keypoints(seq, copy=True)

        for f in range(3):
            np.testing.assert_allclose(out[f, 0], seq[3, 0])
        for f in range(8, 10):
            np.testing.assert_allclose(out[f, 0], seq[7, 0])

    def test_completely_missing_landmark(self):
        seq = np.zeros((10, 94, 4), dtype=np.float32)
        seq[:, 0] = [1.0, 2.0, 3.0, 1.0]

        out = interpolate_keypoints(seq, copy=True)
        self.assertTrue((out[:, 10] == 0.0).all())

    def test_copy_semantics(self):
        seq = np.zeros((5, 94, 4), dtype=np.float32)
        seq[0, 0] = [1.0, 1.0, 1.0, 1.0]
        seq[4, 0] = [5.0, 5.0, 5.0, 1.0]

        out = interpolate_keypoints(seq, copy=True)
        self.assertEqual(seq[2, 0, 3], 0.0)
        self.assertGreater(out[2, 0, 3], 0.0)

    def test_batched_interpolation(self):
        batch = np.zeros((2, 10, 94, 4), dtype=np.float32)
        for b in range(2):
            for f in range(10):
                batch[b, f, 0] = [float(f), float(f), float(f), 1.0]
            batch[b, 4, 0] = [0.0, 0.0, 0.0, 0.0]

        out = interpolate_keypoints(batch, copy=True)
        self.assertEqual(out.shape, (2, 10, 94, 4))
        for b in range(2):
            np.testing.assert_allclose(out[b, 4, 0, 0], 4.0)


if __name__ == "__main__":
    unittest.main()
