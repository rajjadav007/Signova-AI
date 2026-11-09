"""
Custom exceptions for the Signova AI video input and landmark extraction pipeline.
"""


class VideoPipelineError(Exception):
    """Base exception for all video pipeline errors."""
    pass


class VideoNotFoundError(VideoPipelineError, FileNotFoundError):
    """Raised when the specified video file path does not exist."""
    pass


class UnsupportedVideoFormatError(VideoPipelineError, ValueError):
    """Raised when the video format/extension is not supported."""
    pass


class CorruptedVideoError(VideoPipelineError, RuntimeError):
    """Raised when a video file is corrupted or cannot be decoded."""
    pass


class EmptyVideoError(VideoPipelineError, ValueError):
    """Raised when a video contains zero readable frames."""
    pass


class LandmarkExtractionError(VideoPipelineError, RuntimeError):
    """Raised when MediaPipe landmark extraction fails."""
    pass


class ModelAssetNotFoundError(VideoPipelineError, FileNotFoundError):
    """Raised when the MediaPipe model asset file (.task) cannot be found."""
    pass
