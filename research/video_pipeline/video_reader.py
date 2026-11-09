"""
Video reader module for decoding video files frame-by-frame with OpenCV.
"""

from pathlib import Path
from typing import Any, Dict, Generator, Optional, Tuple, Union
import cv2
import numpy as np

from .config import SUPPORTED_FORMATS
from .exceptions import (
    CorruptedVideoError,
    EmptyVideoError,
    UnsupportedVideoFormatError,
    VideoNotFoundError,
)


class VideoReader:
    """
    Decodes video files frame-by-frame as RGB images using OpenCV.
    Provides streaming generator yielding (frame_index, rgb_frame).
    """

    def __init__(self, video_path: Union[str, Path]):
        self._cap: Optional[cv2.VideoCapture] = None
        self.video_path = Path(video_path).resolve()
        self._validate_file()

        self._cap: Optional[cv2.VideoCapture] = cv2.VideoCapture(str(self.video_path))
        if not self._cap.isOpened():
            self.release()
            raise CorruptedVideoError(f"OpenCV could not open video: {self.video_path}")

        self.fps: float = float(self._cap.get(cv2.CAP_PROP_FPS))
        self.frame_count: int = int(self._cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.width: int = int(self._cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height: int = int(self._cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.duration_seconds: float = (
            round(self.frame_count / self.fps, 3) if self.fps > 0 and self.frame_count > 0 else 0.0
        )

        self._validate_stream()

    def _validate_file(self) -> None:
        """Validate file existence, format extension, and non-zero size."""
        if not self.video_path.exists():
            raise VideoNotFoundError(f"Video file not found: {self.video_path}")

        if not self.video_path.is_file():
            raise VideoNotFoundError(f"Path is not a regular file: {self.video_path}")

        ext = self.video_path.suffix.lower()
        if ext not in SUPPORTED_FORMATS:
            raise UnsupportedVideoFormatError(
                f"Unsupported video format '{ext}'. Supported formats: {sorted(SUPPORTED_FORMATS)}"
            )

        if self.video_path.stat().st_size == 0:
            raise EmptyVideoError(f"Video file is 0 bytes (empty): {self.video_path}")

    def _validate_stream(self) -> None:
        """Verify video contains at least one decodable frame."""
        # Some video formats or corrupted files report frame_count <= 0 or invalid resolution
        if self.frame_count <= 0 or self.width <= 0 or self.height <= 0:
            ret, frame = self._cap.read()
            if not ret or frame is None or frame.size == 0:
                self.release()
                raise EmptyVideoError(f"Video contains no decodable frames: {self.video_path}")
            # Reset cursor back to start
            self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            if self.frame_count <= 0:
                self.frame_count = 1

    def get_metadata(self) -> Dict[str, Any]:
        """Return metadata summary for the video file."""
        return {
            "video_path": str(self.video_path),
            "video_name": self.video_path.name,
            "format": self.video_path.suffix.lower(),
            "width": self.width,
            "height": self.height,
            "resolution": f"{self.width}x{self.height}",
            "fps": round(self.fps, 2),
            "frame_count": self.frame_count,
            "duration_seconds": self.duration_seconds,
            "file_size_bytes": self.video_path.stat().st_size,
        }

    def read_frames(self) -> Generator[Tuple[int, np.ndarray], None, None]:
        """
        Yields (frame_index, rgb_frame) sequentially.
        Converts BGR to RGB format required by MediaPipe.
        Raises CorruptedVideoError if a frame fails mid-stream.
        """
        if self._cap is None or not self._cap.isOpened():
            raise CorruptedVideoError("Video capture is closed or uninitialized.")

        self._cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        frame_idx = 0

        while True:
            ret, frame = self._cap.read()
            if not ret:
                # If we haven't reached expected frame_count and stream terminated abruptly
                if self.frame_count > 0 and frame_idx < self.frame_count:
                    # Some containers report a slightly inaccurate frame_count (+-1), check if frame_idx > 0
                    if frame_idx == 0:
                        raise EmptyVideoError(f"Could not read any frames from: {self.video_path}")
                break

            if frame is None or frame.size == 0:
                raise CorruptedVideoError(
                    f"Corrupted frame encountered at index {frame_idx} in: {self.video_path}"
                )

            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            yield frame_idx, rgb_frame
            frame_idx += 1

        if frame_idx == 0:
            raise EmptyVideoError(f"Zero frames could be read from video: {self.video_path}")

    def release(self) -> None:
        """Safely release OpenCV VideoCapture resource."""
        if hasattr(self, "_cap") and self._cap is not None:
            if self._cap.isOpened():
                self._cap.release()
            self._cap = None

    def __enter__(self) -> "VideoReader":
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()

    def __del__(self) -> None:
        self.release()
