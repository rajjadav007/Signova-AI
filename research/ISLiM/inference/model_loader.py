"""
Model loader module for ISLiM standalone inference application.
"""

from pathlib import Path
from typing import Dict, Any, Tuple, Optional, Union
import logging
import torch
import numpy as np
from transformers import T5Tokenizer

import sys
_INFERENCE_DIR = Path(__file__).resolve().parent
_ISLIM_DIR = _INFERENCE_DIR.parent
if str(_ISLIM_DIR) not in sys.path:
    sys.path.insert(0, str(_ISLIM_DIR))

from src.islim.model import ISLiMModel
from inference.config import InferenceConfig, ModelConfig, DEFAULT_CHECKPOINT, DEFAULT_TOKENIZER
from inference.exceptions import ModelLoadingError

logger = logging.getLogger("islim.inference.model_loader")


def register_safe_globals() -> None:
    """Register numpy scalar and ndarray types for safe weights_only=True loading."""
    safe_types = [
        np.core.multiarray.scalar,
        np.dtype,
        np.ndarray,
        np.core.multiarray._reconstruct,
        np.dtypes.Float64DType,
    ]
    torch.serialization.add_safe_globals(safe_types)


def resolve_device(requested_device: str = "auto") -> torch.device:
    """
    Resolve requested device string to a concrete torch.device.
    Falls back gracefully to CPU if CUDA is unavailable.
    """
    req = requested_device.lower().strip()
    if req in ("auto", "cuda", "cuda:0", "gpu"):
        if torch.cuda.is_available():
            return torch.device("cuda:0")
        logger.warning("CUDA requested or set to auto, but not available. Falling back to CPU.")
        return torch.device("cpu")
    elif req == "cpu":
        return torch.device("cpu")
    else:
        try:
            dev = torch.device(requested_device)
            if dev.type == "cuda" and not torch.cuda.is_available():
                logger.warning(f"Device {dev} not available. Falling back to CPU.")
                return torch.device("cpu")
            return dev
        except Exception as e:
            raise ModelLoadingError(f"Invalid device specification: {requested_device} ({e})") from e


class ModelArtifacts:
    """Container holding initialized model, tokenizer, device, and metadata."""
    def __init__(
        self,
        model: ISLiMModel,
        tokenizer: T5Tokenizer,
        device: torch.device,
        checkpoint_epoch: Optional[int] = None,
        checkpoint_path: Optional[Path] = None,
    ):
        self.model = model
        self.tokenizer = tokenizer
        self.device = device
        self.checkpoint_epoch = checkpoint_epoch
        self.checkpoint_path = checkpoint_path

    def to(self, device: Union[str, torch.device]) -> "ModelArtifacts":
        """Move model to new device."""
        target = resolve_device(str(device)) if isinstance(device, str) else device
        self.model = self.model.to(target)
        self.device = target
        return self


def load_islim_model(
    checkpoint_path: Optional[Union[str, Path]] = None,
    tokenizer_dir: Optional[Union[str, Path]] = None,
    device: str = "auto",
    model_config: Optional[ModelConfig] = None,
) -> ModelArtifacts:
    """
    Safely load pretrained ISLiM model and local tokenizer.
    
    Args:
        checkpoint_path: Path to .pt checkpoint. Defaults to official checkpoint.
        tokenizer_dir: Directory containing local t5-small assets.
        device: 'auto', 'cuda', or 'cpu'.
        model_config: ModelConfig instance (defaults to corrected num_query_tokens=0).
        
    Returns:
        ModelArtifacts container ready for inference.
    """
    register_safe_globals()
    
    ckpt_path = Path(checkpoint_path) if checkpoint_path else DEFAULT_CHECKPOINT
    tok_dir = Path(tokenizer_dir) if tokenizer_dir else DEFAULT_TOKENIZER
    cfg = model_config or ModelConfig()

    if not ckpt_path.exists():
        raise ModelLoadingError(f"Checkpoint file does not exist: {ckpt_path}")
    if not tok_dir.exists():
        raise ModelLoadingError(f"Tokenizer directory does not exist: {tok_dir}")

    # 1. Resolve device
    target_device = resolve_device(device)

    # 2. Load tokenizer
    try:
        tokenizer = T5Tokenizer.from_pretrained(str(tok_dir), local_files_only=True)
    except Exception as e:
        raise ModelLoadingError(f"Failed to load local T5Tokenizer from {tok_dir}: {e}") from e

    # 3. Instantiate model with corrected configuration (num_query_tokens=0)
    try:
        model_dict = cfg.to_islim_dict(str(tok_dir))
        model = ISLiMModel(model_dict)
    except Exception as e:
        raise ModelLoadingError(f"Failed to initialize ISLiMModel architecture: {e}") from e

    # 4. Safe checkpoint loading with weights_only=True
    try:
        checkpoint = torch.load(ckpt_path, map_location="cpu", weights_only=True)
    except Exception as e:
        raise ModelLoadingError(f"Failed to load checkpoint safely with weights_only=True: {e}") from e

    if "model_state_dict" not in checkpoint:
        raise ModelLoadingError(f"Checkpoint {ckpt_path} missing 'model_state_dict' key.")

    # 5. Load weights with strict=False and inspect key mismatches
    incompatible = model.load_state_dict(checkpoint["model_state_dict"], strict=False)
    
    # Documented permissible missing keys: query_tokens or legacy projection layers when num_query_tokens=0
    # Documented permissible unexpected keys: unused loss heads or training-only state
    if incompatible.missing_keys:
        logger.info(f"Loaded with missing keys (non-operational): {incompatible.missing_keys}")
    if incompatible.unexpected_keys:
        logger.info(f"Loaded with unexpected keys (legacy training): {incompatible.unexpected_keys}")

    # 6. Evaluation mode and gradient freeze
    model.eval()
    for param in model.parameters():
        param.requires_grad = False

    # 7. Move to target device
    model = model.to(target_device)
    epoch = checkpoint.get("epoch", None)

    return ModelArtifacts(
        model=model,
        tokenizer=tokenizer,
        device=target_device,
        checkpoint_epoch=epoch,
        checkpoint_path=ckpt_path,
    )
