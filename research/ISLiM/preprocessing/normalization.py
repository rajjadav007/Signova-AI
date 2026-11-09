"""
ISLiM spatial coordinate min-max normalization.

Faithfully reproduces research/ISLiM/src/data/dataset.py:
  - Independent per-sequence, per-channel min-max normalization for x, y, and z.
  - Formula: (arr - arr.min()) / (arr.max() - arr.min()) when range > 1e-8.
  - Constant coordinates (range <= 1e-8) become arr - arr.min() (i.e. 0.0).
  - Visibility (channel 3) is strictly preserved without modification.
"""

import numpy as np

EPSILON = 1e-8


def _normalize_single(keypoints: np.ndarray) -> np.ndarray:
    """Normalize single sequence of shape (T, 94, 4)."""
    x = keypoints[:, :, 0:1]
    y = keypoints[:, :, 1:2]
    z = keypoints[:, :, 2:3]

    for arr in (x, y, z):
        rng = float(arr.max() - arr.min())
        if rng > EPSILON:
            arr[...] = (arr - arr.min()) / rng
        else:
            arr[...] = arr - arr.min()

    keypoints[:, :, :3] = np.concatenate([x, y, z], axis=2)
    return keypoints


def normalize_coordinates(kp_seq: np.ndarray, copy: bool = True) -> np.ndarray:
    """
    Min-max normalize x, y, z coordinate channels to [0, 1].
    
    Args:
        kp_seq: Array of shape (T, 94, 4) or (B, T, 94, 4).
        copy: Whether to copy input array before normalizing.
        
    Returns:
        Normalized array with identical shape.
    """
    if copy:
        kp_seq = np.array(kp_seq, copy=True, dtype=np.float32)
    else:
        kp_seq = kp_seq.astype(np.float32, copy=False)

    if kp_seq.ndim == 3:
        return _normalize_single(kp_seq)
    elif kp_seq.ndim == 4:
        for b in range(kp_seq.shape[0]):
            _normalize_single(kp_seq[b])
        return kp_seq
    else:
        raise ValueError(f"Expected 3D or 4D array, got {kp_seq.ndim}D.")

