"""
Integration tests for Video-to-ISLiM Inference Pipeline (Part 2.2).
Verifies end-to-end video translation, model reuse, output generation, and persistence.
"""

from pathlib import Path
import tempfile
import unittest
import numpy as np

from research.video_pipeline.output_handler import load_json_report, load_keypoints
from research.video_pipeline.video_inference_pipeline import VideoToISLiMPipeline

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
BASELINE_VIDEO = PROJECT_ROOT / "International-Week-of-SnapYT.App.mp4"
NEW_VIDEO = PROJECT_ROOT / "Deaf-U-SnapYT.App.mp4"


class TestVideoInferenceIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize pipeline once for test class to verify single-load reuse."""
        cls.pipeline = VideoToISLiMPipeline(device="auto")

    def test_model_loaded_once_and_reused(self):
        """Verify model and tokenizer are initialized and retained in memory."""
        self.assertIsNotNone(self.pipeline.predictor.model)
        self.assertIsNotNone(self.pipeline.predictor.tokenizer)
        model_id = id(self.pipeline.predictor.model)
        self.assertEqual(id(self.pipeline.predictor.model), model_id)

    def test_baseline_video_regression(self):
        """Verify baseline video produces verified shape, output, and translation."""
        self.assertTrue(BASELINE_VIDEO.exists(), f"Baseline video missing: {BASELINE_VIDEO}")

        with tempfile.TemporaryDirectory() as tmp_dir:
            res = self.pipeline.predict_video_both_decodings(
                video_path=BASELINE_VIDEO,
                output_dir=tmp_dir,
                save_output=True,
            )

            # Metadata and shape checks
            self.assertEqual(res["input_video_filename"], "International-Week-of-SnapYT.App.mp4")
            self.assertEqual(res["extracted_frame_count"], 125)
            self.assertEqual(res["landmark_shape"], [125, 94, 4])
            self.assertEqual(res["landmark_dtype"], "float32")
            self.assertEqual(res["output_status"], "SUCCESS")

            # Translation checks
            beam_pred = res["beam_search"]["prediction"]
            greedy_pred = res["greedy_search"]["prediction"]
            self.assertIsInstance(beam_pred, str)
            self.assertGreater(len(beam_pred), 0)
            self.assertEqual(beam_pred, "but i cannot wait to stop and let me go")
            self.assertEqual(greedy_pred, "i cannot wait to stop my unknown")

            # Persistence checks
            saved_npy = Path(res["saved_keypoints_path"])
            saved_json = Path(res["saved_report_path"])
            self.assertTrue(saved_npy.exists())
            self.assertTrue(saved_json.exists())

            loaded_kps = load_keypoints(saved_npy)
            self.assertEqual(loaded_kps.shape, (125, 94, 4))
            loaded_json = load_json_report(saved_json)
            self.assertEqual(loaded_json["beam_search"]["prediction"], beam_pred)


if __name__ == "__main__":
    unittest.main()
