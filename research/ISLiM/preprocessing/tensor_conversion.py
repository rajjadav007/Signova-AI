"""
ISLiM PyTorch tensor conversion and dimension layout formatting.

Converts normalized 128-frame keypoint arrays to the official model tensor format:
  - Single sequence: (128, 94, 4) -> (4, 94, 128) [C, K, T]
  - Batched / default: (B, 4, 94, 128) [B, C, K, T] float32
"""

from typing import Optional, Union
import numpy as np
import torch


def convert_to_tensor(
    keypoints: Union[np.ndarray, torch.Tensor],
    add_batch_dim: bool = True,
    device: Optional[Union[str, torch.device]] = None,
) -> torch.Tensor:
    """
    Convert (128, 94, 4) or (B, 128, 94, 4) array to (B, 4, 94, 128) tensor.
    
    Args:
        keypoints: Array or tensor of shape (128, 94, 4) or (B, 128, 94, 4).
        add_batch_dim: If True and input is 3D, adds batch dim -> (1, 4, 94, 128).
        device: Target torch device (CPU/CUDA).
        
    Returns:
        torch.Tensor of shape (B, 4, 94, 128) or (4, 94, 128) as float32.
    """
    if isinstance(keypoints, np.ndarray):
        tensor = torch.from_numpy(keypoints).float()
    elif isinstance(keypoints, torch.Tensor):
        tensor = keypoints.float()
    else:
        tensor = torch.tensor(keypoints, dtype=torch.float32)

    # 3D: (T=128, K=94, C=4) -> permute to (C=4, K=94, T=128)
    if tensor.ndim == 3:
        if tensor.shape == (4, 94, 128):
            pass  # already in (C, K, T)
        elif tensor.shape == (128, 94, 4):
            tensor = tensor.permute(2, 1, 0)  # (4, 94, 128)
        else:
            raise ValueError(f"Unexpected 3D tensor shape {tuple(tensor.shape)}, expected (128, 94, 4) or (4, 94, 128).")

        if add_batch_dim:
            tensor = tensor.unsqueeze(0)  # (1, 4, 94, 128)

    # 4D: (B, T=128, K=94, C=4) -> permute to (B, C=4, K=94, T=128)
    elif tensor.ndim == 4:
        if tensor.shape[1] == 4 and tensor.shape[2] == 94 and tensor.shape[3] == 128:
            pass  # already in (B, 4, 94, 128)
        elif tensor.shape[1] == 128 and tensor.shape[2] == 94 and tensor.shape[3] == 4:
            tensor = tensor.permute(0, 3, 2, 1)  # (B, 4, 94, 128)
        else:
            raise ValueError(f"Unexpected 4D tensor shape {tuple(tensor.shape)}, expected (B, 128, 94, 4) or (B, 4, 94, 128).")

    else:
        raise ValueError(f"Expected 3D or 4D tensor, got {tensor.ndim}D.")

    if device is not None:
        tensor = tensor.to(device)

    return tensor

