"""
Output handler module for ISLiM standalone inference application.

Structures and formats predictions, metadata, and timing metrics into clean JSON.
"""

from typing import Dict, Any, List, Optional, Union
from pathlib import Path
import json


def format_prediction_result(
    prediction: Union[str, List[str]],
    token_ids: Union[List[int], List[List[int]]],
    device: str,
    preprocessing_time_ms: float,
    inference_time_ms: float,
    input_shape: List[int],
    model_input_shape: List[int],
    decoding_strategy: str = "beam",
    model_name: str = "ISLiM",
    accuracy_verified: bool = False,
    extra_metadata: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Construct a standardized inference result dictionary.
    """
    total_time_ms = round(preprocessing_time_ms + inference_time_ms, 2)
    
    result = {
        "success": True,
        "prediction": prediction,
        "token_ids": token_ids,
        "device": device,
        "decoding_strategy": decoding_strategy,
        "preprocessing_time_ms": round(preprocessing_time_ms, 2),
        "inference_time_ms": round(inference_time_ms, 2),
        "total_time_ms": total_time_ms,
        "input_shape": list(input_shape),
        "model_input_shape": list(model_input_shape),
        "model": model_name,
        "accuracy_verified": accuracy_verified,
        "note": "Translation accuracy is unverified without ground-truth subtitles/labels." if not accuracy_verified else "Verified against ground-truth.",
    }
    
    if extra_metadata:
        result["metadata"] = extra_metadata
        
    return result


def format_error_result(
    error: Exception,
    device: str = "unknown",
    preprocessing_time_ms: float = 0.0,
    inference_time_ms: float = 0.0,
    input_shape: Optional[List[int]] = None,
) -> Dict[str, Any]:
    """Construct a standardized error result dictionary."""
    total_time_ms = round(preprocessing_time_ms + inference_time_ms, 2)
    return {
        "success": False,
        "error": str(error),
        "error_type": type(error).__name__,
        "prediction": None,
        "token_ids": [],
        "device": device,
        "preprocessing_time_ms": round(preprocessing_time_ms, 2),
        "inference_time_ms": round(inference_time_ms, 2),
        "total_time_ms": total_time_ms,
        "input_shape": list(input_shape) if input_shape else None,
        "model": "ISLiM",
        "accuracy_verified": False,
    }


def save_result_to_json(result: Dict[str, Any], output_path: Union[str, Path], indent: int = 2) -> Path:
    """Save structured result dictionary to a JSON file."""
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=indent)
    return path
