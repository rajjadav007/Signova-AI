"""
Custom exceptions for ISLiM standalone inference application.
"""


class ISLiMInferenceError(Exception):
    """Base exception for all ISLiM inference errors."""
    pass


class ModelLoadingError(ISLiMInferenceError):
    """Raised when model weights or tokenizer fail to load."""
    pass


class InvalidInputError(ISLiMInferenceError):
    """Raised when input keypoints fail validation."""
    pass


class PreprocessingError(ISLiMInferenceError):
    """Raised when preprocessing pipeline fails on keypoints."""
    pass


class PredictionError(ISLiMInferenceError):
    """Raised during model execution or text decoding."""
    pass
