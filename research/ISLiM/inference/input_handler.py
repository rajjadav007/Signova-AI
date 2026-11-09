"""
Input handler module for ISLiM standalone inference application.

Validates and loads raw landmark sequences from .npy files or NumPy arrays.
"""

from pathlib import Path
from typing import Union, Tuple, List
import numpy as np

from inference.exceptions import InvalidInputError


NUM_LANDMARKS = 94
NUM_CHANNELS = 4


def validate_keypoint_array(arr: np.ndarray) -> np.ndarray:
    """
    Validate landmark sequence array.
    Supports (T, 94, 4) or (B, T, 94, 4).
    
    Returns:
        Validated float32 numpy array.
        
    Raises:
        InvalidInputError: If array violates shape, dtype, or value constraints.
    """
    if not isinstance(arr, np.ndarray):
        raise InvalidInputError(f"Expected numpy.ndarray, got {type(arr).__name__}.")

    if arr.size == 0:
        raise InvalidInputError("Keypoint array is empty (size is 0).")

    # Reject non-numeric
    if not np.issubdtype(arr.dtype, np.number):
        raise InvalidInputError(f"Keypoint array must contain numeric data, got {arr.dtype}.")

    # Reject NaN and Inf
    if np.isnan(arr).any():
        raise InvalidInputError("Keypoint array contains NaN (Not a Number) values.")
    if np.isinf(arr).any():
        raise InvalidInputError("Keypoint array contains infinite (Inf/-Inf) values.")

    # Shape validation
    if arr.ndim == 3:
        # (T, K, C)
        T, K, C = arr.shape
        if T < 1:
            raise InvalidInputError(f"Sequence has invalid frame length: T={T} (must be >= 1).")
        if K != NUM_LANDMARKS:
            raise InvalidInputError(
                f"Incorrect landmark count: expected {NUM_LANDMARKS} landmarks, got {K}."
            )
        if C != NUM_CHANNELS:
            raise InvalidInputError(
                f"Incorrect channel count: expected {NUM_CHANNELS} channels (x, y, z, vis), got {C}."
            )
    elif arr.ndim == 4:
        # (B, T, K, C)
        B, T, K, C = arr.shape
        if B < 1:
            raise InvalidInputError(f"Batch has invalid batch size: B={B} (must be >= 1).")
        if T < 1:
            raise InvalidInputError(f"Batch sequence has invalid frame length: T={T} (must be >= 1).")
        if K != NUM_LANDMARKS:
            raise InvalidInputError(
                f"Incorrect landmark count in batch: expected {NUM_LANDMARKS} landmarks, got {K}."
            )
        if C != NUM_CHANNELS:
            raise InvalidInputError(
                f"Incorrect channel count in batch: expected {NUM_CHANNELS} channels, got {C}."
            )
    else:
        raise InvalidInputError(
            f"Invalid keypoint array dimension: expected 3D (T, 94, 4) or 4D (B, T, 94, 4), got {arr.ndim}D with shape {arr.shape}."
        )

    # Cast to float32 without modifying original
    return arr.astype(np.float32, copy=True)


def load_keypoints_from_file(file_path: Union[str, Path]) -> np.ndarray:
    """
    Safely load keypoints from a .npy file.
    
    Args:
        file_path: Path to the .npy file.
        
    Returns:
        Validated float32 numpy array.
        
    Raises:
        InvalidInputError: If file is missing, not a .npy file, or fails validation.
    """
    path = Path(file_path)

    if not path.exists():
        raise InvalidInputError(f"Input file not found: {path}")

    if not path.is_file():
        raise InvalidInputError(f"Input path is not a file: {path}")

    if path.suffix.lower() != ".npy":
        raise InvalidInputError(
            f"Unsupported file format '{path.suffix}'. Only NumPy '.npy' files are supported. "
            "Raw video files must be converted to landmarks before inference."
        )

    try:
        data = np.load(path, allow_pickle=False)
    except ValueError as e:
        raise InvalidInputError(f"Security error: cannot load {path} (pickle objects forbidden): {e}") from e
    except Exception as e:
        raise InvalidInputError(f"Failed to load keypoints from {path}: {e}") from e

    return validate_keypoint_array(data)


def resolve_input(input_data: Union[str, Path, np.ndarray]) -> np.ndarray:
    """
    Dispatch and validate input from either a file path or a NumPy array.
    """
    if isinstance(input_data, (str, Path)):
        return load_keypoints_from_file(input_data)
    elif isinstance(input_data, np.ndarray):
        return validate_keypoint_array(input_data)
    else:
        raise InvalidInputError(
            f"Unsupported input type '{type(input_data).__name__}'. "
            "Expected a file path (str/Path) to a .npy file or a numpy.ndarray."
        )
