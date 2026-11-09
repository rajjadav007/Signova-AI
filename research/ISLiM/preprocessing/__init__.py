"""
ISLiM Preprocessing Package for Signova AI.

Provides the complete, verified input data pipeline matching official ISLiM training:
  1. Landmark validation
  2. Missing landmark temporal interpolation (gaps <= 5)
  3. Per-channel min-max spatial coordinate normalization
  4. Temporal resampling / zero-padding to 128 frames
  5. Tensor layout formatting to (B, 4, 94, 128) float32
"""

from typing import Optional, Union, Tuple
import numpy as np
import torch

from .landmark_mapping import (
    NUM_LANDMARKS,
    NUM_CHANNELS,
    POSE_INDICES,
    FACE_LIPS,
    FACE_EYES,
    FACE_EYEBROWS,
    FACE_INDICES,
    GROUP_SLICES,
    get_landmark_group,
    extract_holistic_frame,
)
from .validation import (
    PreprocessingValidationError,
    validate_sequence,
    assert_valid_sequence,
)
from .interpolation import (
    MAX_MISSING_CONSECUTIVE,
    interpolate_keypoints,
)
from .normalization import (
    EPSILON,
    normalize_coordinates,
)
from .temporal_processing import (
    TARGET_FRAMES,
    resample_temporal,
)
from .tensor_conversion import (
    convert_to_tensor,
)


def preprocess_sequence(
    raw_sequence: Union[np.ndarray, list],
    add_batch_dim: bool = True,
    device: Optional[Union[str, torch.device]] = None,
) -> torch.Tensor:
    """
    Execute full ISLiM preprocessing pipeline.
    
    Args:
        raw_sequence: Input landmark sequence (T, 94, 4) or (B, T, 94, 4).
        add_batch_dim: Whether to prepend batch dimension for 3D input -> (1, 4, 94, 128).
        device: Target torch device (CPU or CUDA).
        
    Returns:
        torch.Tensor of shape (B, 4, 94, 128) or (4, 94, 128) float32.
    """
    # 1. Validate
    validated = assert_valid_sequence(raw_sequence)

    # 2. Interpolate missing landmarks (<= 5 frames)
    interpolated = interpolate_keypoints(validated, copy=True)

    # 3. Spatial min-max normalization
    normalized = normalize_coordinates(interpolated, copy=False)

    # 4. Temporal resizing to 128 frames
    resampled, _ = resample_temporal(normalized, target_frames=TARGET_FRAMES)

    # 5. Format to official tensor layout
    tensor = convert_to_tensor(resampled, add_batch_dim=add_batch_dim, device=device)

    return tensor


__all__ = [
    "NUM_LANDMARKS",
    "NUM_CHANNELS",
    "POSE_INDICES",
    "FACE_LIPS",
    "FACE_EYES",
    "FACE_EYEBROWS",
    "FACE_INDICES",
    "GROUP_SLICES",
    "get_landmark_group",
    "extract_holistic_frame",
    "PreprocessingValidationError",
    "validate_sequence",
    "assert_valid_sequence",
    "MAX_MISSING_CONSECUTIVE",
    "interpolate_keypoints",
    "EPSILON",
    "normalize_coordinates",
    "TARGET_FRAMES",
    "resample_temporal",
    "convert_to_tensor",
    "preprocess_sequence",
]

