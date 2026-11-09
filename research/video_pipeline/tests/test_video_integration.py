"""
Integration test running the video pipeline on the real sample video.
Compares extracted landmarks against Phase 1.7.1 baseline for numerical parity.
"""

from pathlib import Path
import tempfile
import unittest
import numpy as np

from research.video_pipeline.config import VideoPipelineConfig
from research.video_pipeline.output_handler import load_json_report, load_keypoints
from research.video_pipeline.video_processor import VideoProcessor

SAMPLE_VIDEO = Path(__file__).resolve().parent.parent.parent.parent / "International-Week-of-SnapYT.App.mp4"
PHASE1_BASELINE_NPY = Path(__file__).resolve().parent.parent.parent / "ISLiM" / "results" / "real_video_keypoints.npy"


class TestVideoIntegration(unittest.TestCase):
    def test_sample_video_integration_and_parity(self):
        """
        Process International-Week-of-SnapYT.App.mp4 and verify:
        1. Shape is (125, 94, 4).
        2. Dtype is float32.
        3. Parity with Phase 1.7.1 baseline keypoints.
        4. Detection statistics match expected values.
        """
        self.assertTrue(SAMPLE_VIDEO.exists(), f"Sample video not found at: {SAMPLE_VIDEO}")

        with tempfile.TemporaryDirectory() as tmp_dir:
            output_dir = Path(tmp_dir) / "results"
            cfg = VideoPipelineConfig(results_dir=output_dir)
            processor = VideoProcessor(cfg)

            kps, report = processor.process_video(SAMPLE_VIDEO, output_dir=output_dir, save_output=True)

            # 1. Shape and dtype verification
            self.assertIsInstance(kps, np.ndarray)
            self.assertEqual(kps.shape, (125, 94, 4))
            self.assertEqual(kps.dtype, np.float32)

            # 2. Report verification
            self.assertEqual(report["original_video_filename"], "International-Week-of-SnapYT.App.mp4")
            self.assertEqual(report["processed_frames"], 125)
            self.assertEqual(report["frame_count"], 125)
            self.assertEqual(report["fps"], 30.0)
            self.assertEqual(report["resolution"], "360x360")
            self.assertEqual(report["extraction_status"], "SUCCESS")
            self.assertEqual(report["total_landmark_instances"], 125 * 94)

            # 3. Detection statistics verification
            detection_rates = report["subsystem_detection_rates"]
            self.assertEqual(detection_rates["pose_detected_frames"], 125)
            self.assertEqual(detection_rates["pose_detection_percentage"], 100.0)
            self.assertEqual(detection_rates["face_detected_frames"], 125)
            self.assertEqual(detection_rates["face_detection_percentage"], 100.0)
            self.assertEqual(detection_rates["right_hand_detected_frames"], 120)
            self.assertEqual(detection_rates["right_hand_detection_percentage"], 96.0)
            self.assertEqual(detection_rates["left_hand_detected_frames"], 110)
            self.assertEqual(detection_rates["left_hand_detection_percentage"], 88.0)

            self.assertEqual(report["missing_landmark_count"], 420)
            self.assertEqual(report["present_landmark_count"], 11330)
            self.assertEqual(report["landmark_presence_percentage"], 96.43)

            # 4. Verify saved file can be safely reloaded
            saved_npy = output_dir / "International-Week-of-SnapYT.App_keypoints.npy"
            self.assertTrue(saved_npy.exists())
            reloaded_kps = load_keypoints(saved_npy)
            self.assertTrue(np.array_equal(kps, reloaded_kps))

            saved_json = output_dir / "International-Week-of-SnapYT.App_extraction_report.json"
            self.assertTrue(saved_json.exists())
            reloaded_json = load_json_report(saved_json)
            self.assertEqual(reloaded_json["landmark_presence_percentage"], 96.43)

            # 5. Numerical parity with Phase 1.7.1 baseline
            if PHASE1_BASELINE_NPY.exists():
                phase1_kps = np.load(str(PHASE1_BASELINE_NPY), allow_pickle=False)
                self.assertEqual(phase1_kps.shape, (125, 94, 4))

                diff = np.abs(kps - phase1_kps)
                max_diff = float(np.max(diff))
                mean_diff = float(np.mean(diff))

                # MediaPipe HolisticLandmarker running on identical frames should have exact or near-identical parity (< 1e-4)
                self.assertLess(max_diff, 1e-4, f"Discrepancy with Phase 1.7.1 baseline: max diff = {max_diff}")
                self.assertLess(mean_diff, 1e-6, f"Mean discrepancy with Phase 1.7.1 baseline: mean diff = {mean_diff}")


if __name__ == "__main__":
    unittest.main()
