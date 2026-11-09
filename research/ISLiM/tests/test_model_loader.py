"""
Unit tests for ISLiM Model Loader (Part 1.9).
"""

from pathlib import Path
import sys
import unittest
import torch

TEST_DIR = Path(__file__).resolve().parent
ISLIM_DIR = TEST_DIR.parent
if str(ISLIM_DIR) not in sys.path:
    sys.path.insert(0, str(ISLIM_DIR))

from inference.model_loader import load_islim_model, resolve_device, ModelArtifacts
from inference.exceptions import ModelLoadingError
from inference.config import DEFAULT_CHECKPOINT, DEFAULT_TOKENIZER


class TestModelLoader(unittest.TestCase):
    def test_resolve_device(self):
        """Verify device resolution and graceful fallback."""
        cpu_dev = resolve_device("cpu")
        self.assertEqual(cpu_dev.type, "cpu")

        auto_dev = resolve_device("auto")
        expected_type = "cuda" if torch.cuda.is_available() else "cpu"
        self.assertEqual(auto_dev.type, expected_type)

    def test_model_loading_success(self):
        """Verify model and tokenizer load successfully with corrected configuration."""
        artifacts = load_islim_model(device="cpu")
        self.assertIsInstance(artifacts, ModelArtifacts)
        self.assertIsNotNone(artifacts.model)
        self.assertIsNotNone(artifacts.tokenizer)
        self.assertEqual(artifacts.device.type, "cpu")

        # Check evaluation mode
        self.assertFalse(artifacts.model.training)

        # Check gradients frozen
        for p in artifacts.model.parameters():
            self.assertFalse(p.requires_grad)

        # Check corrected configuration (num_query_tokens == 0)
        self.assertEqual(artifacts.model.visual_encoder.num_query_tokens, 0)

    def test_model_loading_missing_checkpoint(self):
        """Verify error raised on invalid checkpoint path."""
        with self.assertRaises(ModelLoadingError) as ctx:
            load_islim_model(checkpoint_path=ISLIM_DIR / "non_existent.pt")
        self.assertIn("does not exist", str(ctx.exception))

    def test_model_loading_missing_tokenizer(self):
        """Verify error raised on invalid tokenizer directory."""
        with self.assertRaises(ModelLoadingError) as ctx:
            load_islim_model(tokenizer_dir=ISLIM_DIR / "non_existent_assets")
        self.assertIn("does not exist", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
