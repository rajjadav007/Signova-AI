"""
ISLiM landmark sequence validation.

Validates:
  - Non-empty sequence
  - Dimensionality (T, 94, 4) or (B, T, 94, 4)
  - Numeric integrity (finite, no NaN, no Inf)
  - Visibility bounds
"""

from typing import Optional, Tuple
import numpy as np

from .landmark_mapping import NUM_LANDMARKS, NUM_CHANNELS


class PreprocessingValidationError(ValueError):
    """Raised when landmark sequence violates input contract."""
    pass


def validate_sequence(arr: np.ndarray) -> Tuple[bool, Optional[str]]:
    """
    Validate landmark array contract without raising exception.
    Returns (is_valid, error_message).
    """
    if arr is None:
        return False, "Input array is None."

    if not isinstance(arr, (np.ndarray, list)):
        return False, f"Expected numpy.ndarray, got {type(arr).__name__}."

    if not isinstance(arr, np.ndarray):
        try:
            arr = np.asarray(arr)
        except Exception as e:
            return False, f"Failed converting input to numpy array: {e}."

    if arr.size == 0:
        return False, "Input sequence is empty."

    # Shape checks: allow (T, 94, 4) or (B, T, 94, 4) or (94, 4)
    if arr.ndim not in (2, 3, 4):
        return False, f"Expected 2D (94, 4), 3D (T, 94, 4), or 4D (B, T, 94, 4) shape, got {arr.ndim}D with shape {arr.shape}."

    if arr.shape[-2] != NUM_LANDMARKS:
        return False, f"Expected exactly {NUM_LANDMARKS} landmarks at axis -2, got {arr.shape[-2]} (shape: {arr.shape})."

    if arr.shape[-1] != NUM_CHANNELS:
        return False, f"Expected exactly {NUM_CHANNELS} channels [x, y, z, vis] at axis -1, got {arr.shape[-1]} (shape: {arr.shape})."

    # Sequence length check
    if arr.ndim == 3 and arr.shape[0] < 1:
        return False, "Sequence length T must be >= 1."
    if arr.ndim == 4 and (arr.shape[0] < 1 or arr.shape[1] < 1):
        return False, "Batch dimension B and sequence length T must be >= 1."

    # Numeric integrity: no NaNs, no Infs
    if not np.isfinite(arr).all():
        nan_count = int(np.isnan(arr).sum())
        inf_count = int(np.isinf(arr).sum())
        return False, f"Non-finite numeric values detected: {nan_count} NaNs, {inf_count} Infs."

    # Visibility checks: channel index 3
    vis = arr[..., 3]
    if (vis < 0.0).any() or (vis > 1.05).any():  # slight float tolerance
        min_v = float(vis.min())
        max_v = float(vis.max())
        return False, f"Visibility values outside expected range [0.0, 1.0]: min={min_v:.4f}, max={max_v:.4f}."

    return True, None


def assert_valid_sequence(arr: np.ndarray) -> np.ndarray:
    """
    Assert landmark sequence validity. Raises PreprocessingValidationError if invalid.
    Returns array as float32.
    """
    is_valid, err = validate_sequence(arr)
    if not is_valid:
        raise PreprocessingValidationError(err)
    if not isinstance(arr, np.ndarray):
        arr = np.asarray(arr)
    return arr.astype(np.float32, copy=False)

