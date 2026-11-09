"""
Predictor module for ISLiM standalone inference application.

Provides the core ISLiMPredictor class for executing sign language translation.
"""

from pathlib import Path
from typing import Union, Dict, Any, Optional, List
import time
import numpy as np
import torch

import sys
_INFERENCE_DIR = Path(__file__).resolve().parent
_ISLIM_DIR = _INFERENCE_DIR.parent
if str(_ISLIM_DIR) not in sys.path:
    sys.path.insert(0, str(_ISLIM_DIR))

from preprocessing import preprocess_sequence
from inference.config import InferenceConfig, DecodingConfig, ModelConfig
from inference.model_loader import load_islim_model, ModelArtifacts, resolve_device
from inference.input_handler import resolve_input
from inference.output_handler import format_prediction_result, format_error_result
from inference.exceptions import (
    ISLiMInferenceError,
    InvalidInputError,
    PreprocessingError,
    PredictionError,
)


class ISLiMPredictor:
    """
    Main reusable predictor for Indian Sign Language translation using ISLiM.
    
    Loads the model once upon initialization and executes inference repeatedly.
    """

    def __init__(
        self,
        checkpoint_path: Optional[Union[str, Path]] = None,
        tokenizer_dir: Optional[Union[str, Path]] = None,
        device: str = "auto",
        model_config: Optional[ModelConfig] = None,
        default_decoding: Optional[DecodingConfig] = None,
    ):
        """
        Initialize the predictor and load model artifacts once.
        """
        self.config = InferenceConfig(
            checkpoint_path=Path(checkpoint_path) if checkpoint_path else InferenceConfig.checkpoint_path,
            tokenizer_dir=Path(tokenizer_dir) if tokenizer_dir else InferenceConfig.tokenizer_dir,
            device=device,
            model_config=model_config or ModelConfig(),
            decoding=default_decoding or DecodingConfig(),
        )
        
        # Load model and tokenizer once
        self.artifacts: ModelArtifacts = load_islim_model(
            checkpoint_path=self.config.checkpoint_path,
            tokenizer_dir=self.config.tokenizer_dir,
            device=self.config.device,
            model_config=self.config.model_config,
        )
        self.model = self.artifacts.model
        self.tokenizer = self.artifacts.tokenizer
        self.device = self.artifacts.device

    def to(self, device: str) -> "ISLiMPredictor":
        """Move predictor to a different device (e.g. 'cpu' or 'cuda')."""
        self.artifacts.to(device)
        self.device = self.artifacts.device
        return self

    def predict(
        self,
        keypoints: Union[str, Path, np.ndarray],
        decoding: str = "beam",
        max_length: int = 128,
        num_beams: int = 4,
        repetition_penalty: float = 1.5,
        no_repeat_ngram_size: int = 3,
        length_penalty: float = 1.2,
    ) -> Dict[str, Any]:
        """
        Translate sign language keypoints to English text.
        
        Args:
            keypoints: Path to .npy file or raw numpy array of shape (T, 94, 4) or (B, T, 94, 4).
            decoding: 'beam' or 'greedy'.
            max_length: Maximum target sequence token length.
            num_beams: Number of beams for beam search.
            repetition_penalty: Penalty for repeating tokens.
            no_repeat_ngram_size: Avoid repeating n-grams of this size.
            length_penalty: Exponential penalty to sequence length.
            
        Returns:
            Structured result dictionary with clean text, token IDs, and timing metrics.
        """
        t_prep_start = time.perf_counter()
        
        # 1. Resolve and validate input
        try:
            raw_array = resolve_input(keypoints)
        except InvalidInputError:
            raise
        except Exception as e:
            raise InvalidInputError(f"Input handling failed: {e}") from e

        original_shape = list(raw_array.shape)
        is_batched = (raw_array.ndim == 4)

        # 2. Preprocess sequence
        try:
            tensor = preprocess_sequence(raw_array, add_batch_dim=True, device=self.device)
        except Exception as e:
            raise PreprocessingError(f"Preprocessing pipeline failed: {e}") from e

        t_prep_end = time.perf_counter()
        prep_time_ms = (t_prep_end - t_prep_start) * 1000.0

        model_input_shape = list(tensor.shape)

        # 3. Configure generation
        decoding_strategy = decoding.lower().strip()
        if decoding_strategy not in ("beam", "greedy"):
            raise PredictionError(f"Unsupported decoding strategy '{decoding}'. Must be 'beam' or 'greedy'.")

        if decoding_strategy == "greedy":
            gen_kwargs = {
                "max_length": max_length,
                "num_beams": 1,
                "do_sample": False,
            }
        else:
            gen_kwargs = {
                "max_length": max_length,
                "num_beams": num_beams,
                "repetition_penalty": repetition_penalty,
                "no_repeat_ngram_size": no_repeat_ngram_size,
                "length_penalty": length_penalty,
                "early_stopping": True,
                "do_sample": False,
            }

        # 4. Model inference
        if self.device.type == "cuda":
            torch.cuda.synchronize(self.device)
        t_inf_start = time.perf_counter()

        try:
            with torch.inference_mode():
                # Visual encoder generates visual tokens (B, T_frames, d_model)
                visual_embeddings = self.model.visual_encoder.get_sequence_output(tensor)

                # T5 autoregressive generation
                output_token_ids = self.model.t5.generate(
                    inputs_embeds=visual_embeddings,
                    **gen_kwargs,
                )
        except Exception as e:
            raise PredictionError(f"Model generation failed: {e}") from e

        if self.device.type == "cuda":
            torch.cuda.synchronize(self.device)
        t_inf_end = time.perf_counter()
        inf_time_ms = (t_inf_end - t_inf_start) * 1000.0

        # 5. Decode tokens
        token_ids_list = output_token_ids.cpu().tolist()

        if is_batched:
            predictions = [
                self.tokenizer.decode(ids, skip_special_tokens=True).strip()
                for ids in token_ids_list
            ]
            final_pred = predictions
            final_tokens = token_ids_list
        else:
            final_pred = self.tokenizer.decode(token_ids_list[0], skip_special_tokens=True).strip()
            final_tokens = token_ids_list[0]

        # 6. Build structured output
        return format_prediction_result(
            prediction=final_pred,
            token_ids=final_tokens,
            device=str(self.device),
            preprocessing_time_ms=prep_time_ms,
            inference_time_ms=inf_time_ms,
            input_shape=original_shape,
            model_input_shape=model_input_shape,
            decoding_strategy=decoding_strategy,
            model_name="ISLiM",
            accuracy_verified=False,
        )
