"""
Unit tests for VideoProcessor class.
Tests end-to-end processing, output persistence, statistics calculation, and error propagation.
"""

from pathlib import Path
import tempfile
import unittest
import cv2
import numpy as np

from research.video_pipeline.config import VideoPipelineConfig
from research.video_pipeline.exceptions import EmptyVideoError, VideoNotFoundError
from research.video_pipeline.output_handler import load_json_report, load_keypoints
from research.video_pipeline.video_processor import VideoProcessor


def create_test_video(path: Path, num_frames: int = 5, width: int = 64, height: int = 64) -> Path:
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(path), fourcc, 10.0, (width, height))
    for i in range(num_frames):
        frame = np.full((height, width, 3), i * 30, dtype=np.uint8)
        out.write(frame)
    out.release()
    return path


class TestVideoProcessor(unittest.TestCase):
    def test_video_processor_synthetic_run(self):
        """Test VideoProcessor on synthetic video with output persistence."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            video_path = Path(tmp_dir) / "test_synth.mp4"
            create_test_video(video_path, num_frames=6, width=64, height=64)

            results_dir = Path(tmp_dir) / "results"
            cfg = VideoPipelineConfig(results_dir=results_dir)
            processor = VideoProcessor(cfg)

            kps, report = processor.process_video(video_path, output_dir=results_dir, save_output=True)

            # Validate output array
            self.assertIsInstance(kps, np.ndarray)
            self.assertEqual(kps.shape, (6, 94, 4))
            self.assertEqual(kps.dtype, np.float32)

            # Validate report contents
            self.assertEqual(report["original_video_filename"], "test_synth.mp4")
            self.assertEqual(report["processed_frames"], 6)
            self.assertEqual(report["frame_count"], 6)
            self.assertEqual(report["landmark_sequence_shape"], [6, 94, 4])
            self.assertEqual(report["data_type"], "float32")
            self.assertEqual(report["extraction_status"], "SUCCESS")
            self.assertIn("extraction_duration", report)
            self.assertIn("missing_landmark_count", report)
            self.assertIn("landmark_presence_percentage", report)

            # Validate saved artifacts
            npy_file = results_dir / "test_synth_keypoints.npy"
            json_file = results_dir / "test_synth_extraction_report.json"
            self.assertTrue(npy_file.exists())
            self.assertTrue(json_file.exists())

            # Test load with allow_pickle=False
            loaded_kps = load_keypoints(npy_file)
            self.assertTrue(np.array_equal(kps, loaded_kps))
            self.assertEqual(loaded_kps.dtype, np.float32)

            loaded_json = load_json_report(json_file)
            self.assertEqual(loaded_json["original_video_filename"], "test_synth.mp4")
            self.assertEqual(loaded_json["landmark_sequence_shape"], [6, 94, 4])

    def test_video_processor_missing_video(self):
        """Test VideoProcessor raises VideoNotFoundError on missing file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            processor = VideoProcessor()
            with self.assertRaises(VideoNotFoundError):
                processor.process_video(Path(tmp_dir) / "non_existent.mp4")

    def test_video_processor_empty_video(self):
        """Test VideoProcessor raises EmptyVideoError on 0-byte video."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            empty_vid = Path(tmp_dir) / "empty.mp4"
            empty_vid.touch()

            processor = VideoProcessor()
            with self.assertRaises(EmptyVideoError):
                processor.process_video(empty_vid)


if __name__ == "__main__":
    unittest.main()
