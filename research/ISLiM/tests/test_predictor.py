"""
Unit and functional tests for ISLiMPredictor (Part 1.9).
"""

from pathlib import Path
import sys
import unittest
import numpy as np

TEST_DIR = Path(__file__).resolve().parent
ISLIM_DIR = TEST_DIR.parent
if str(ISLIM_DIR) not in sys.path:
    sys.path.insert(0, str(ISLIM_DIR))

from inference.predictor import ISLiMPredictor
from inference.exceptions import InvalidInputError, PredictionError


class TestPredictor(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Load predictor once for all tests in this class on CPU."""
        cls.predictor = ISLiMPredictor(device="cpu")

    def test_predictor_initialization(self):
        """Verify predictor initializes and loads artifacts."""
        self.assertIsNotNone(self.predictor.model)
        self.assertIsNotNone(self.predictor.tokenizer)
        self.assertEqual(self.predictor.device.type, "cpu")

    def test_predict_single_sequence(self):
        """Verify prediction on single synthetic sequence of 60 frames."""
        arr = np.random.rand(60, 94, 4).astype(np.float32)
        res = self.predictor.predict(arr, decoding="greedy")
        self.assertTrue(res["success"])
        self.assertIsInstance(res["prediction"], str)
        self.assertGreater(len(res["prediction"]), 0)
        self.assertGreater(len(res["token_ids"]), 0)
        self.assertEqual(res["input_shape"], [60, 94, 4])
        self.assertEqual(res["model_input_shape"], [1, 4, 94, 128])

    def test_predict_exact_128_frames(self):
        """Verify prediction on sequence with exactly 128 frames."""
        arr = np.random.rand(128, 94, 4).astype(np.float32)
        res = self.predictor.predict(arr, decoding="greedy")
        self.assertTrue(res["success"])
        self.assertEqual(res["input_shape"], [128, 94, 4])
        self.assertEqual(res["model_input_shape"], [1, 4, 94, 128])

    def test_predict_long_sequence(self):
        """Verify prediction on sequence longer than 128 frames (e.g. 180 frames)."""
        arr = np.random.rand(180, 94, 4).astype(np.float32)
        res = self.predictor.predict(arr, decoding="greedy")
        self.assertTrue(res["success"])
        self.assertEqual(res["input_shape"], [180, 94, 4])
        self.assertEqual(res["model_input_shape"], [1, 4, 94, 128])

    def test_predict_batched_sequence(self):
        """Verify prediction on batch of sequences (B=2, T=50, 94, 4)."""
        batch_arr = np.random.rand(2, 50, 94, 4).astype(np.float32)
        res = self.predictor.predict(batch_arr, decoding="greedy")
        self.assertTrue(res["success"])
        self.assertIsInstance(res["prediction"], list)
        self.assertEqual(len(res["prediction"]), 2)
        self.assertEqual(res["model_input_shape"], [2, 4, 94, 128])

    def test_predict_beam_vs_greedy(self):
        """Verify beam search and greedy decoding both execute."""
        arr = np.random.rand(50, 94, 4).astype(np.float32)
        res_greedy = self.predictor.predict(arr, decoding="greedy")
        res_beam = self.predictor.predict(arr, decoding="beam")
        self.assertTrue(res_greedy["success"])
        self.assertTrue(res_beam["success"])
        self.assertEqual(res_greedy["decoding_strategy"], "greedy")
        self.assertEqual(res_beam["decoding_strategy"], "beam")

    def test_predict_invalid_input(self):
        """Verify invalid input raises InvalidInputError."""
        with self.assertRaises(InvalidInputError):
            self.predictor.predict(np.zeros((10, 50, 4), dtype=np.float32))

    def test_predict_invalid_decoding_strategy(self):
        """Verify unsupported decoding strategy raises PredictionError."""
        arr = np.random.rand(50, 94, 4).astype(np.float32)
        with self.assertRaises(PredictionError) as ctx:
            self.predictor.predict(arr, decoding="nucleus")
        self.assertIn("Unsupported decoding strategy", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
