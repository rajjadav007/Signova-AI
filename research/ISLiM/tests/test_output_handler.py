"""
Unit tests for ISLiM Output Handler (Part 1.9).
"""

from pathlib import Path
import sys
import json
import tempfile
import unittest

TEST_DIR = Path(__file__).resolve().parent
ISLIM_DIR = TEST_DIR.parent
if str(ISLIM_DIR) not in sys.path:
    sys.path.insert(0, str(ISLIM_DIR))

from inference.output_handler import (
    format_prediction_result,
    format_error_result,
    save_result_to_json,
)


class TestOutputHandler(unittest.TestCase):
    def test_format_prediction_result(self):
        """Verify structured output contains all required fields and correct timing math."""
        res = format_prediction_result(
            prediction="hello world",
            token_ids=[0, 123, 456, 1],
            device="cuda:0",
            preprocessing_time_ms=4.52,
            inference_time_ms=250.15,
            input_shape=[85, 94, 4],
            model_input_shape=[1, 4, 94, 128],
            decoding_strategy="beam",
            model_name="ISLiM",
            accuracy_verified=False,
        )

        self.assertTrue(res["success"])
        self.assertEqual(res["prediction"], "hello world")
        self.assertEqual(res["token_ids"], [0, 123, 456, 1])
        self.assertEqual(res["device"], "cuda:0")
        self.assertEqual(res["preprocessing_time_ms"], 4.52)
        self.assertEqual(res["inference_time_ms"], 250.15)
        self.assertEqual(res["total_time_ms"], 254.67)
        self.assertEqual(res["input_shape"], [85, 94, 4])
        self.assertEqual(res["model_input_shape"], [1, 4, 94, 128])
        self.assertFalse(res["accuracy_verified"])
        self.assertIn("unverified", res["note"].lower())

    def test_format_error_result(self):
        """Verify error result handles exceptions safely."""
        err = ValueError("Invalid input tensor")
        res = format_error_result(
            error=err,
            device="cpu",
            preprocessing_time_ms=1.2,
            inference_time_ms=0.0,
            input_shape=[10, 94, 4],
        )
        self.assertFalse(res["success"])
        self.assertEqual(res["error"], "Invalid input tensor")
        self.assertEqual(res["error_type"], "ValueError")
        self.assertIsNone(res["prediction"])
        self.assertEqual(res["token_ids"], [])

    def test_save_result_to_json(self):
        """Verify saving to JSON file."""
        res = {"success": True, "prediction": "test sentence", "total_time_ms": 100.5}
        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            tmp_path = Path(tmp.name)
        try:
            out = save_result_to_json(res, tmp_path)
            self.assertTrue(out.exists())
            with open(out, "r", encoding="utf-8") as f:
                loaded = json.load(f)
            self.assertEqual(loaded["prediction"], "test sentence")
        finally:
            if tmp_path.exists():
                tmp_path.unlink()


if __name__ == "__main__":
    unittest.main()
