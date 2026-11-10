"""
Preprocessor for isolated ISL recognition sequences.
Resamples raw MediaPipe (T, 94, 4) or (T, 94, 3) landmarks to a fixed sequence (30, 282)
with scale-invariant body centering and spatial normalization.
"""

from typing import Optional, Tuple, Union
import numpy as np
import torch

TARGET_FRAMES: int = 30
NUM_KEYPOINTS: int = 94
FEATURE_DIM: int = NUM_KEYPOINTS * 3  # 94 * 3 = 282 (x, y, z)


class IsolatedSignPreprocessor:
    """Standardizes temporal and spatial landmark sequences for isolated gesture models."""

    def __init__(self, target_frames: int = TARGET_FRAMES) -> None:
        self.target_frames = target_frames
        self.feature_dim = FEATURE_DIM

    def resample_temporal(self, sequence: np.ndarray) -> np.ndarray:
        """
        Resample sequence along time axis to exactly target_frames.
        
        Args:
            sequence: array of shape (T, num_features)
        Returns:
            resampled: array of shape (target_frames, num_features)
        """
        T, D = sequence.shape
        if T == self.target_frames:
            return sequence.astype(np.float32)

        if T == 0:
            return np.zeros((self.target_frames, D), dtype=np.float32)

        if T == 1:
            # Single static frame: repeat across all target frames
            return np.repeat(sequence, self.target_frames, axis=0).astype(np.float32)

        # Linear interpolation across time indices
        orig_indices = np.linspace(0, T - 1, num=T)
        target_indices = np.linspace(0, T - 1, num=self.target_frames)
        
        resampled = np.empty((self.target_frames, D), dtype=np.float32)
        for d in range(D):
            resampled[:, d] = np.interp(target_indices, orig_indices, sequence[:, d])
            
        return resampled

    def normalize_spatial(self, landmarks_3d: np.ndarray) -> np.ndarray:
        """
        Center landmarks relative to torso midpoint (shoulders) and scale by bounding span.
        
        Args:
            landmarks_3d: shape (T, 94, 3)
        Returns:
            normalized: shape (T, 94, 3) float32
        """
        T, K, C = landmarks_3d.shape
        normalized = landmarks_3d.copy()

        for t in range(T):
            frame = normalized[t]  # (94, 3)
            # Check if pose shoulders exist (indices 0 and 1 correspond to shoulders in ISLiM 6-pose subset)
            # Shoulders: left shoulder = 0, right shoulder = 1
            torso_pts = frame[0:2]
            valid_torso = np.any(torso_pts != 0.0)

            if valid_torso:
                center = np.mean(torso_pts, axis=0, keepdims=True)
            else:
                # Fallback to mean of non-zero landmarks
                non_zeros = frame[np.any(frame != 0.0, axis=-1)]
                if len(non_zeros) > 0:
                    center = np.mean(non_zeros, axis=0, keepdims=True)
                else:
                    center = np.zeros((1, 3), dtype=np.float32)

            frame_centered = frame - center

            # Compute bounding scale
            non_zeros_centered = frame_centered[np.any(frame != 0.0, axis=-1)]
            if len(non_zeros_centered) > 0:
                scale = np.max(np.abs(non_zeros_centered)) + 1e-6
                frame_normalized = frame_centered / scale
            else:
                frame_normalized = frame_centered

            normalized[t] = frame_normalized

        return normalized.astype(np.float32)

    def process(
        self,
        raw_keypoints: Union[np.ndarray, torch.Tensor],
    ) -> torch.Tensor:
        """
        Full preprocessing pipeline:
        1. Extract (x, y, z) coordinates (discarding visibility for model input).
        2. Normalize spatial coordinates.
        3. Flatten 94*3 -> 282 features per frame.
        4. Resample temporal length to target_frames (30).
        
        Args:
            raw_keypoints: shape (T, 94, 4) or (T, 94, 3) or (T, 282)
        Returns:
            tensor: torch.FloatTensor of shape (1, 30, 282)
        """
        if isinstance(raw_keypoints, torch.Tensor):
            arr = raw_keypoints.detach().cpu().numpy()
        else:
            arr = np.array(raw_keypoints, dtype=np.float32)

        if arr.ndim == 2 and arr.shape[1] == self.feature_dim:
            # Already flattened (T, 282)
            seq_282 = arr
        elif arr.ndim == 3 and arr.shape[1] == NUM_KEYPOINTS:
            # (T, 94, 4) or (T, 94, 3)
            coords_3d = arr[:, :, :3]  # take x, y, z
            norm_3d = self.normalize_spatial(coords_3d)
            seq_282 = norm_3d.reshape(arr.shape[0], self.feature_dim)
        elif arr.ndim == 2 and arr.shape[1] == NUM_KEYPOINTS * 4:
            # (T, 376)
            reshaped = arr.reshape(-1, NUM_KEYPOINTS, 4)[:, :, :3]
            norm_3d = self.normalize_spatial(reshaped)
            seq_282 = norm_3d.reshape(-1, self.feature_dim)
        else:
            raise ValueError(
                f"Unexpected landmark input shape {arr.shape}. "
                f"Expected (T, 94, 4), (T, 94, 3), or (T, 282)."
            )

        # Resample time dimension to target_frames
        resampled_282 = self.resample_temporal(seq_282)

        # Return as batch tensor (1, target_frames, 282)
        try:
            tensor = torch.from_numpy(resampled_282).unsqueeze(0).float()
        except Exception:
            tensor = torch.tensor(resampled_282.tolist(), dtype=torch.float32).unsqueeze(0)
        return tensor


preprocessor = IsolatedSignPreprocessor()
