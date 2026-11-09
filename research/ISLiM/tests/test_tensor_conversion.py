"""
Unit tests for ISLiM tensor conversion and full end-to-end preprocessing pipeline.
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

from preprocessing.tensor_conversion import convert_to_tensor
from preprocessing import preprocess_sequence, PreprocessingValidationError


class TestTensorConversion(unittest.TestCase):
    def test_convert_to_tensor_single_batched(self):
        arr = np.random.uniform(0.0, 1.0, size=(128, 94, 4)).astype(np.float32)
        t = convert_to_tensor(arr, add_batch_dim=True)

        self.assertIsInstance(t, torch.Tensor)
        self.assertEqual(t.shape, (1, 4, 94, 128))
        self.assertEqual(t.dtype, torch.float32)

        # Verify channel permute: t[0, c, k, frame] == arr[frame, k, c]
        self.assertEqual(float(t[0, 0, 10, 20]), float(arr[20, 10, 0]))
        self.assertEqual(float(t[0, 1, 10, 20]), float(arr[20, 10, 1]))
        self.assertEqual(float(t[0, 2, 10, 20]), float(arr[20, 10, 2]))
        self.assertEqual(float(t[0, 3, 10, 20]), float(arr[20, 10, 3]))

    def test_convert_to_tensor_unbatched(self):
        arr = np.random.uniform(0.0, 1.0, size=(128, 94, 4)).astype(np.float32)
        t = convert_to_tensor(arr, add_batch_dim=False)

        self.assertIsInstance(t, torch.Tensor)
        self.assertEqual(t.shape, (4, 94, 128))
        self.assertEqual(t.dtype, torch.float32)

    def test_convert_to_tensor_batched(self):
        arr_b = np.random.uniform(0.0, 1.0, size=(3, 128, 94, 4)).astype(np.float32)
        t = convert_to_tensor(arr_b)

        self.assertIsInstance(t, torch.Tensor)
        self.assertEqual(t.shape, (3, 4, 94, 128))
        self.assertEqual(t.dtype, torch.float32)

    def test_end_to_end_pipeline_short(self):
        # 45 frames input
        raw = np.random.uniform(-10.0, 10.0, size=(45, 94, 4)).astype(np.float32)
        raw[:, :, 3] = 1.0
        raw[10:14, 0] = 0.0

        tensor = preprocess_sequence(raw, add_batch_dim=True)
        self.assertIsInstance(tensor, torch.Tensor)
        self.assertEqual(tensor.shape, (1, 4, 94, 128))
        self.assertEqual(tensor.dtype, torch.float32)

        self.assertGreaterEqual(float(tensor[:, :3].min()), 0.0)
        self.assertLessEqual(float(tensor[:, :3].max()), 1.0)

    def test_end_to_end_pipeline_long(self):
        # 210 frames input
        raw = np.random.uniform(0.0, 100.0, size=(210, 94, 4)).astype(np.float32)
        raw[:, :, 3] = 0.9

        tensor = preprocess_sequence(raw, add_batch_dim=True)
        self.assertEqual(tensor.shape, (1, 4, 94, 128))
        self.assertEqual(tensor.dtype, torch.float32)

    def test_end_to_end_pipeline_batched(self):
        raw_b = np.random.uniform(0.0, 50.0, size=(2, 85, 94, 4)).astype(np.float32)
        raw_b[:, :, :, 3] = 1.0

        tensor = preprocess_sequence(raw_b)
        self.assertEqual(tensor.shape, (2, 4, 94, 128))
        self.assertEqual(tensor.dtype, torch.float32)

    def test_end_to_end_invalid_rejection(self):
        raw_nan = np.random.uniform(0.0, 1.0, size=(30, 94, 4)).astype(np.float32)
        raw_nan[5, 10, 0] = np.nan

        with self.assertRaises(PreprocessingValidationError):
            preprocess_sequence(raw_nan)


if __name__ == "__main__":
    unittest.main()
