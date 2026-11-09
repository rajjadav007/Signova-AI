"""
Unit tests for ISLiM temporal processing and 128-frame resampling.
"""

import sys
import unittest
from pathlib import Path
import numpy as np
import torch

# Ensure research/ISLiM is on sys.path
TEST_DIR = Path(__file__).resolve().parent
PROJECT_DIR = TEST_DIR.parent
if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

from preprocessing.temporal_processing import resample_temporal, TARGET_FRAMES


class TestTemporalProcessing(unittest.TestCase):
    def test_shorter_sequence_padding(self):
        T_short = 50
        seq = np.ones((T_short, 94, 4), dtype=np.float32)
        out, valid_frames = resample_temporal(seq, target_frames=TARGET_FRAMES)

        self.assertEqual(out.shape, (128, 94, 4))
        self.assertEqual(valid_frames, 50)
        np.testing.assert_allclose(out[:50], 1.0)
        np.testing.assert_allclose(out[50:], 0.0)

    def test_exact_sequence_length(self):
        seq = np.random.uniform(0.0, 1.0, size=(128, 94, 4)).astype(np.float32)
        out, valid_frames = resample_temporal(seq, target_frames=TARGET_FRAMES)

        self.assertEqual(out.shape, (128, 94, 4))
        self.assertEqual(valid_frames, 128)
        np.testing.assert_allclose(out, seq)

    def test_longer_sequence_downsampling(self):
        T_long = 250
        seq = np.zeros((T_long, 94, 4), dtype=np.float32)
        for t in range(T_long):
            seq[t, :, 0] = float(t)

        out, valid_frames = resample_temporal(seq, target_frames=TARGET_FRAMES)

        self.assertEqual(out.shape, (128, 94, 4))
        self.assertEqual(valid_frames, 128)
        self.assertEqual(out[0, 0, 0], 0.0)
        self.assertEqual(out[-1, 0, 0], 249.0)

        expected_indices = torch.linspace(0, T_long - 1, TARGET_FRAMES).long().numpy()
        np.testing.assert_allclose(out[:, 0, 0], expected_indices.astype(np.float32))

    def test_torch_tensor_support(self):
        tensor_short = torch.ones((30, 94, 4), dtype=torch.float32)
        out_t, valid_f = resample_temporal(tensor_short, target_frames=128)

        self.assertIsInstance(out_t, torch.Tensor)
        self.assertEqual(out_t.shape, (128, 94, 4))
        self.assertEqual(valid_f, 30)
        self.assertTrue((out_t[:30] == 1.0).all())
        self.assertTrue((out_t[30:] == 0.0).all())

    def test_batched_temporal_resampling(self):
        batch_short = np.ones((3, 40, 94, 4), dtype=np.float32)
        out, valid_f = resample_temporal(batch_short, target_frames=128)

        self.assertEqual(out.shape, (3, 128, 94, 4))
        self.assertEqual(valid_f, 40)
        self.assertTrue((out[:, :40] == 1.0).all())
        self.assertTrue((out[:, 40:] == 0.0).all())

        batch_long = np.ones((2, 180, 94, 4), dtype=np.float32)
        out_l, valid_fl = resample_temporal(batch_long, target_frames=128)
        self.assertEqual(out_l.shape, (2, 128, 94, 4))
        self.assertEqual(valid_fl, 128)


if __name__ == "__main__":
    unittest.main()
