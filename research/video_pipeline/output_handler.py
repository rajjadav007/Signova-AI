"""
Output handler for saving and loading landmark sequences and JSON reports.
"""

import json
from pathlib import Path
from typing import Any, Dict, Union
import numpy as np

from .config import KEYPOINT_COORDS, NUM_KEYPOINTS


def save_keypoints(keypoints: np.ndarray, output_path: Union[str, Path]) -> Path:
    """
    Save landmark sequence to a NumPy .npy file with allow_pickle=False.
    Validates that array has shape (T, 94, 4) and float32 dtype.
    """
    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    if not isinstance(keypoints, np.ndarray):
        raise TypeError(f"Expected numpy.ndarray, got {type(keypoints)}")

    if keypoints.ndim != 3 or keypoints.shape[1] != NUM_KEYPOINTS or keypoints.shape[2] != KEYPOINT_COORDS:
        raise ValueError(
            f"Invalid keypoints shape {keypoints.shape}. Expected (T, {NUM_KEYPOINTS}, {KEYPOINT_COORDS})."
        )

    if keypoints.dtype != np.float32:
        raise TypeError(f"Expected float32 dtype, got {keypoints.dtype}")

    # Ensure suffix is .npy
    if out_file.suffix.lower() != ".npy":
        out_file = out_file.with_suffix(".npy")

    np.save(str(out_file), keypoints, allow_pickle=False)
    return out_file


def load_keypoints(npy_path: Union[str, Path]) -> np.ndarray:
    """
    Load landmark sequence from .npy file with allow_pickle=False and validate structure.
    """
    file_path = Path(npy_path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"Keypoint file not found: {file_path}")

    arr = np.load(str(file_path), allow_pickle=False)

    if arr.ndim != 3 or arr.shape[1] != NUM_KEYPOINTS or arr.shape[2] != KEYPOINT_COORDS:
        raise ValueError(
            f"Loaded array shape {arr.shape} does not match (T, {NUM_KEYPOINTS}, {KEYPOINT_COORDS})"
        )

    return arr.astype(np.float32, copy=False)


def save_json_report(report_data: Dict[str, Any], output_path: Union[str, Path]) -> Path:
    """
    Save structured extraction report as formatted JSON.
    """
    out_file = Path(output_path).resolve()
    out_file.parent.mkdir(parents=True, exist_ok=True)

    if out_file.suffix.lower() != ".json":
        out_file = out_file.with_suffix(".json")

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2, ensure_ascii=False)

    return out_file


def load_json_report(json_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Load structured extraction report JSON.
    """
    file_path = Path(json_path).resolve()
    if not file_path.exists():
        raise FileNotFoundError(f"Report file not found: {file_path}")

    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)
