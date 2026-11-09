"""
ISLiM temporal missing-landmark interpolation.

Faithfully reproduces research/ISLiM/scripts/preprocess/extract_keypoints.py:
  - Linear interpolation across gaps <= 5 consecutive missing frames (vis <= 0.5).
  - Sequence boundaries clamp to first/last valid frame coordinates.
  - Gaps > 5 consecutive frames remain zero.
  - Completely missing landmark across all frames remains zero.
"""

from typing import Union
import numpy as np

MAX_MISSING_CONSECUTIVE = 5


def _interpolate_single(kp_seq: np.ndarray, max_missing: int = MAX_MISSING_CONSECUTIVE) -> np.ndarray:
    """Interpolate single sequence of shape (T, K, C)."""
    T, K, C = kp_seq.shape
    if T <= 1:
        kp_seq[kp_seq[:, :, 3] < 0.5] = 0.0
        return kp_seq

    for k in range(K):
        valid = np.where(kp_seq[:, k, 3] > 0.5)[0]
        if len(valid) == 0:
            kp_seq[:, k, :] = 0.0
            continue

        # Interior gaps
        for i in range(len(valid) - 1):
            a, b = valid[i], valid[i + 1]
            gap = b - a
            if 1 < gap <= max_missing:
                for j in range(1, gap):
                    alpha = float(j) / float(gap)
                    kp_seq[a + j, k, :3] = (1.0 - alpha) * kp_seq[a, k, :3] + alpha * kp_seq[b, k, :3]
                    kp_seq[a + j, k, 3] = (1.0 - alpha) * kp_seq[a, k, 3] + alpha * kp_seq[b, k, 3]

        # Sequence boundary replication
        fv, lv = valid[0], valid[-1]
        for f in range(fv):
            if kp_seq[f, k, 3] < 0.5:
                kp_seq[f, k] = kp_seq[fv, k]
        for f in range(lv + 1, T):
            if kp_seq[f, k, 3] < 0.5:
                kp_seq[f, k] = kp_seq[lv, k]

    # Any remaining frames with visibility < 0.5 zeroed out
    kp_seq[kp_seq[:, :, 3] < 0.5] = 0.0
    return kp_seq


def interpolate_keypoints(
    kp_seq: np.ndarray,
    max_missing_consecutive: int = MAX_MISSING_CONSECUTIVE,
    copy: bool = True,
) -> np.ndarray:
    """
    Linearly interpolate missing landmark frames.
    
    Args:
        kp_seq: Array of shape (T, 94, 4) or (B, T, 94, 4).
        max_missing_consecutive: Maximum consecutive frames to interpolate (default 5).
        copy: Whether to copy input array before mutating.
        
    Returns:
        Interpolated array with identical shape.
    """
    if copy:
        kp_seq = np.array(kp_seq, copy=True, dtype=np.float32)
    else:
        kp_seq = kp_seq.astype(np.float32, copy=False)

    if kp_seq.ndim == 3:
        return _interpolate_single(kp_seq, max_missing=max_missing_consecutive)
    elif kp_seq.ndim == 4:
        for b in range(kp_seq.shape[0]):
            _interpolate_single(kp_seq[b], max_missing=max_missing_consecutive)
        return kp_seq
    else:
        raise ValueError(f"Expected 3D or 4D array, got {kp_seq.ndim}D.")

