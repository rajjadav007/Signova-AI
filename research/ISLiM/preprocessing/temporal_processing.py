"""
ISLiM temporal resampling and padding to fixed 128 frames.

Faithfully reproduces research/ISLiM/src/data/dataset.py:
  - If T > 128: Uniform downsampling using torch.linspace(0, T - 1, 128).long()
  - If T < 128: Zero-padding at the end with shape (128 - T, 94, 4)
  - If T == 128: Identity pass-through
"""

from typing import Tuple, Union
import numpy as np
import torch

TARGET_FRAMES = 128


def resample_temporal(
    keypoints: Union[np.ndarray, torch.Tensor],
    target_frames: int = TARGET_FRAMES,
) -> Tuple[Union[np.ndarray, torch.Tensor], int]:
    """
    Resample or pad temporal dimension to target_frames (default 128).
    
    Args:
        keypoints: (T, 94, 4) or (B, T, 94, 4) array or tensor.
        target_frames: Fixed temporal length (128).
        
    Returns:
        (resampled_keypoints, original_valid_frames)
    """
    is_tensor = isinstance(keypoints, torch.Tensor)
    
    # 3D: (T, 94, 4)
    if keypoints.ndim == 3:
        T = keypoints.shape[0]
        K, C = keypoints.shape[1], keypoints.shape[2]
        valid_frames = min(T, target_frames)

        if T > target_frames:
            indices = torch.linspace(0, T - 1, target_frames).long()
            if is_tensor:
                out = keypoints[indices]
            else:
                out = keypoints[indices.numpy()]
        elif T < target_frames:
            pad_len = target_frames - T
            if is_tensor:
                pad = torch.zeros((pad_len, K, C), dtype=keypoints.dtype, device=keypoints.device)
                out = torch.cat([keypoints, pad], dim=0)
            else:
                pad = np.zeros((pad_len, K, C), dtype=keypoints.dtype)
                out = np.concatenate([keypoints, pad], axis=0)
        else:
            out = keypoints

        return out, valid_frames

    # 4D: (B, T, 94, 4)
    elif keypoints.ndim == 4:
        B, T, K, C = keypoints.shape
        valid_frames = min(T, target_frames)

        if T > target_frames:
            indices = torch.linspace(0, T - 1, target_frames).long()
            if is_tensor:
                out = keypoints[:, indices, :, :]
            else:
                out = keypoints[:, indices.numpy(), :, :]
        elif T < target_frames:
            pad_len = target_frames - T
            if is_tensor:
                pad = torch.zeros((B, pad_len, K, C), dtype=keypoints.dtype, device=keypoints.device)
                out = torch.cat([keypoints, pad], dim=1)
            else:
                pad = np.zeros((B, pad_len, K, C), dtype=keypoints.dtype)
                out = np.concatenate([keypoints, pad], axis=1)
        else:
            out = keypoints

        return out, valid_frames

    else:
        raise ValueError(f"Expected 3D or 4D input, got {keypoints.ndim}D.")

