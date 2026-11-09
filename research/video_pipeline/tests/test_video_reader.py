"""
Unit tests for VideoReader class.
Tests valid reading, format validation, error cases, and resource cleanup.
"""

from pathlib import Path
import tempfile
import unittest
import cv2
import numpy as np

from research.video_pipeline.exceptions import (
    CorruptedVideoError,
    EmptyVideoError,
    UnsupportedVideoFormatError,
    VideoNotFoundError,
)
from research.video_pipeline.video_reader import VideoReader

SAMPLE_VIDEO = Path(__file__).resolve().parent.parent.parent.parent / "International-Week-of-SnapYT.App.mp4"


def create_synthetic_video(path: Path, num_frames: int = 5, width: int = 64, height: int = 64) -> Path:
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(path), fourcc, 10.0, (width, height))
    for i in range(num_frames):
        frame = np.full((height, width, 3), i * 40, dtype=np.uint8)
        out.write(frame)
    out.release()
    return path


class TestVideoReader(unittest.TestCase):
    def test_video_reader_valid_sample_video(self):
        """Verify VideoReader correctly parses metadata and frames from the sample video."""
        self.assertTrue(SAMPLE_VIDEO.exists(), f"Sample video not found at {SAMPLE_VIDEO}")

        with VideoReader(SAMPLE_VIDEO) as reader:
            meta = reader.get_metadata()
            self.assertEqual(meta["video_name"], "International-Week-of-SnapYT.App.mp4")
            self.assertEqual(meta["width"], 360)
            self.assertEqual(meta["height"], 360)
            self.assertEqual(meta["fps"], 30.0)
            self.assertEqual(meta["frame_count"], 125)
            self.assertGreater(meta["duration_seconds"], 4.0)

            # Read first 3 frames
            gen = reader.read_frames()
            idx, frame = next(gen)
            self.assertEqual(idx, 0)
            self.assertEqual(frame.shape, (360, 360, 3))
            self.assertEqual(frame.dtype, np.uint8)

    def test_video_reader_synthetic_video(self):
        """Verify VideoReader works on a clean synthetic video."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            video_path = Path(tmp_dir) / "synthetic.mp4"
            create_synthetic_video(video_path, num_frames=10, width=32, height=32)

            with VideoReader(video_path) as reader:
                self.assertEqual(reader.frame_count, 10)
                self.assertEqual(reader.width, 32)
                self.assertEqual(reader.height, 32)
                frames = list(reader.read_frames())
                self.assertEqual(len(frames), 10)
                self.assertEqual(frames[0][0], 0)
                self.assertEqual(frames[9][0], 9)
                self.assertEqual(frames[0][1].shape, (32, 32, 3))

    def test_video_reader_missing_file(self):
        """Verify VideoNotFoundError when video file does not exist."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            missing = Path(tmp_dir) / "does_not_exist.mp4"
            with self.assertRaises(VideoNotFoundError) as ctx:
                VideoReader(missing)
            self.assertIn("not found", str(ctx.exception).lower())

    def test_video_reader_unsupported_format(self):
        """Verify UnsupportedVideoFormatError on invalid extension."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            invalid_ext = Path(tmp_dir) / "test.txt"
            invalid_ext.write_text("not a video")
            with self.assertRaises(UnsupportedVideoFormatError) as ctx:
                VideoReader(invalid_ext)
            self.assertIn("unsupported video format", str(ctx.exception).lower())

    def test_video_reader_empty_video(self):
        """Verify EmptyVideoError on 0-byte video file."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            empty_file = Path(tmp_dir) / "empty.mp4"
            empty_file.touch()
            self.assertEqual(empty_file.stat().st_size, 0)

            with self.assertRaises(EmptyVideoError) as ctx:
                VideoReader(empty_file)
            self.assertIn("empty", str(ctx.exception).lower())

    def test_video_reader_corrupted_file(self):
        """Verify CorruptedVideoError on corrupted non-video content with .mp4 extension."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            corrupted = Path(tmp_dir) / "corrupted.mp4"
            corrupted.write_bytes(b"\x00\x01\x02\x03\x04\x05\x06\x07" * 32)

            with self.assertRaises((CorruptedVideoError, EmptyVideoError)):
                VideoReader(corrupted)

    def test_video_reader_resource_cleanup(self):
        """Verify VideoCapture resource is released after exit."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            video_path = Path(tmp_dir) / "cleanup.mp4"
            create_synthetic_video(video_path, num_frames=3)

            reader = VideoReader(video_path)
            self.assertIsNotNone(reader._cap)
            self.assertTrue(reader._cap.isOpened())

            reader.release()
            self.assertIsNone(reader._cap)

            with VideoReader(video_path) as r2:
                pass
            self.assertIsNone(r2._cap)


if __name__ == "__main__":
    unittest.main()
