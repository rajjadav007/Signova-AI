"""
End-to-End Integration and CLI Tests for ISLiM Standalone Application (Part 1.9).
"""

from pathlib import Path
import sys
import subprocess
import json
import tempfile
import unittest

TEST_DIR = Path(__file__).resolve().parent
ISLIM_DIR = TEST_DIR.parent
if str(ISLIM_DIR) not in sys.path:
    sys.path.insert(0, str(ISLIM_DIR))

from inference.predictor import ISLiMPredictor

REAL_KEYPOINTS_FILE = ISLIM_DIR / "results" / "real_video_keypoints.npy"
PYTHON_EXE = ISLIM_DIR / ".venv" / "Scripts" / "python.exe"


class TestInferencePipeline(unittest.TestCase):
    def test_real_video_keypoints_parity(self):
        """
        Verify real video keypoint translation matches Part 1.7.1 recorded outputs:
        Beam (B=4): 'but i cannot wait to stop and let me go'
        Greedy (B=1): 'i cannot wait to stop my unknown'
        """
        if not REAL_KEYPOINTS_FILE.exists():
            self.skipTest("Real keypoint file missing")

        predictor = ISLiMPredictor(device="auto")

        # 1. Beam search
        res_beam = predictor.predict(REAL_KEYPOINTS_FILE, decoding="beam")
        self.assertTrue(res_beam["success"])
        self.assertEqual(res_beam["prediction"], "but i cannot wait to stop and let me go")
        self.assertEqual(res_beam["input_shape"], [125, 94, 4])
        self.assertEqual(res_beam["model_input_shape"], [1, 4, 94, 128])
        self.assertEqual(
            res_beam["token_ids"],
            [0, 68, 3, 23, 1178, 1749, 12, 1190, 11, 752, 140, 281, 1],
        )

        # 2. Greedy search
        res_greedy = predictor.predict(REAL_KEYPOINTS_FILE, decoding="greedy")
        self.assertTrue(res_greedy["success"])
        self.assertEqual(res_greedy["prediction"], "i cannot wait to stop my unknown")
        self.assertEqual(
            res_greedy["token_ids"],
            [0, 3, 23, 1178, 1749, 12, 1190, 82, 7752, 1],
        )

    def test_standalone_cli_execution(self):
        """Test running standalone_inference.py via subprocess CLI."""
        if not REAL_KEYPOINTS_FILE.exists():
            self.skipTest("Real keypoint file missing")

        cli_script = ISLIM_DIR / "standalone_inference.py"

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as tmp:
            out_json = Path(tmp.name)

        try:
            cmd = [
                str(PYTHON_EXE),
                str(cli_script),
                "--input", str(REAL_KEYPOINTS_FILE),
                "--decoding", "beam",
                "--device", "auto",
                "--output", str(out_json),
            ]
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            self.assertEqual(proc.returncode, 0, f"CLI failed: {proc.stderr}")
            self.assertIn("Prediction", proc.stdout)
            self.assertIn("but i cannot wait to stop and let me go", proc.stdout)

            # Verify written JSON output
            self.assertTrue(out_json.exists())
            with open(out_json, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.assertTrue(data["success"])
            self.assertEqual(data["prediction"], "but i cannot wait to stop and let me go")
            self.assertEqual(data["input_shape"], [125, 94, 4])
        finally:
            if out_json.exists():
                out_json.unlink()

    def test_cli_missing_input_error(self):
        """Test CLI fails cleanly with non-zero exit code on missing input."""
        cli_script = ISLIM_DIR / "standalone_inference.py"
        cmd = [
            str(PYTHON_EXE),
            str(cli_script),
            "--input", "non_existent_keypoints.npy",
        ]
        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn("does not exist", proc.stderr)


if __name__ == "__main__":
    unittest.main()
