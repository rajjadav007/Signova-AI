"""
Configuration module for ISLiM standalone inference application.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, Any, Optional
import os


_INFERENCE_DIR = Path(__file__).resolve().parent
_ISLIM_DIR = _INFERENCE_DIR.parent

DEFAULT_CHECKPOINT = _ISLIM_DIR / "checkpoints" / "ISLiM_full_posestitch_pre_processed.pt"
DEFAULT_TOKENIZER = _ISLIM_DIR / "assets" / "t5-small"


@dataclass
class DecodingConfig:
    """Decoding parameters for T5-small sign-to-text generation."""
    strategy: str = "beam"  # 'beam' or 'greedy'
    max_length: int = 128
    num_beams: int = 4
    repetition_penalty: float = 1.5
    no_repeat_ngram_size: int = 3
    length_penalty: float = 1.2
    early_stopping: bool = True
    do_sample: bool = False

    def to_generate_kwargs(self) -> Dict[str, Any]:
        """Convert to kwargs accepted by HuggingFace T5 generate()."""
        if self.strategy == "greedy":
            return {
                "max_length": self.max_length,
                "num_beams": 1,
                "do_sample": False,
            }
        return {
            "max_length": self.max_length,
            "num_beams": self.num_beams,
            "repetition_penalty": self.repetition_penalty,
            "no_repeat_ngram_size": self.no_repeat_ngram_size,
            "length_penalty": self.length_penalty,
            "early_stopping": self.early_stopping,
            "do_sample": self.do_sample,
        }


@dataclass
class ModelConfig:
    """Corrected architecture parameters matching ISLiM full-frame checkpoint."""
    keypoint_dim: int = 4
    num_keypoints: int = 94
    temporal_channels: list = field(default_factory=lambda: [376, 256, 256])
    temporal_kernel: int = 5
    transformer_embed_dim: int = 512
    transformer_num_heads: int = 8
    transformer_num_layers: int = 4
    transformer_dropout: float = 0.2
    output_dim: int = 512
    max_frames: int = 128
    num_query_tokens: int = 0  # Full-frame mode (verified parity)
    t5_d_model: int = 512
    t5_max_target_len: int = 128

    def to_islim_dict(self, tokenizer_dir: str) -> Dict[str, Any]:
        """Return dict matching ISLiMModel __init__ signature."""
        return {
            "encoder": {
                "keypoint_dim": self.keypoint_dim,
                "num_keypoints": self.num_keypoints,
                "temporal_channels": self.temporal_channels,
                "temporal_kernel": self.temporal_kernel,
                "transformer_embed_dim": self.transformer_embed_dim,
                "transformer_num_heads": self.transformer_num_heads,
                "transformer_num_layers": self.transformer_num_layers,
                "transformer_dropout": self.transformer_dropout,
                "output_dim": self.output_dim,
                "max_frames": self.max_frames,
                "num_query_tokens": self.num_query_tokens,
            },
            "t5": {
                "t5_model": tokenizer_dir,
                "d_model": self.t5_d_model,
                "max_target_len": self.t5_max_target_len,
                "label_smoothing": 0.0,
            },
        }


@dataclass
class InferenceConfig:
    """Top-level configuration for ISLiM standalone inference."""
    checkpoint_path: Path = DEFAULT_CHECKPOINT
    tokenizer_dir: Path = DEFAULT_TOKENIZER
    device: str = "auto"  # 'auto', 'cuda', 'cuda:0', 'cpu'
    model_config: ModelConfig = field(default_factory=ModelConfig)
    decoding: DecodingConfig = field(default_factory=DecodingConfig)
