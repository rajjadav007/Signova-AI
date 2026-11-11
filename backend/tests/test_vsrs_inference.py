"""
Unit tests for VSRS Inference Engine (Signova AI - Step 4).
NOTE: These are structural and mathematical unit tests with synthetic/mock data,
NOT real-world ISL accuracy benchmark evaluations.
"""

from collections import deque
from pathlib import Path
import numpy as np
import pytest

from backend.app.ml.preprocessing.vsrs_preprocessor import TOTAL_FEATURE_DIM, VSRSPreprocessor
from backend.app.ml.recognition.vsrs_inference import (
    DEFAULT_VSRS_CHECKPOINT,
    SUPPORTED_VSRS_CLASSES,
    VSRSInference,
    VSRSInferenceResult,
)


@pytest.fixture
def engine() -> VSRSInference:
    if not DEFAULT_VSRS_CHECKPOINT.exists():
        pytest.skip(f"Checkpoint not found at {DEFAULT_VSRS_CHECKPOINT}")
    inf = VSRSInference(min_confidence=0.65, buffer_size=5)
    inf.reset()
    return inf


class TestVSRSInferenceEngine:
    """Unit test suite for VSRSInference engine and temporal probability aggregation."""

    def test_checkpoint_loading(self, engine: VSRSInference):
        """1. Verify checkpoint loads model, fitted scaler, and exact 11 supported classes."""
        assert engine.is_loaded is True
        assert engine.model is not None
        assert engine.scaler is not None
        assert len(engine.classes) == 11
        assert sorted(engine.classes) == sorted(SUPPORTED_VSRS_CLASSES)

    def test_126_feature_input_validation(self, engine: VSRSInference):
        """2. Verify scaler and model expect exactly 126 input features."""
        assert getattr(engine.scaler, "n_features_in_", None) == TOTAL_FEATURE_DIM
        assert getattr(engine.model, "n_features_in_", None) == TOTAL_FEATURE_DIM

    def test_11_class_probability_output(self, engine: VSRSInference):
        """3. Verify single-frame prediction produces exactly 11 probabilities matching classes."""
        dummy_feat = np.random.randn(TOTAL_FEATURE_DIM).astype(np.float32)
        probs = engine.predict_features_raw(dummy_feat)

        assert isinstance(probs, np.ndarray)
        assert probs.shape == (11,)
        assert np.all(probs >= 0.0)
        assert np.all(probs <= 1.0)

    def test_probability_sum_approx_one(self, engine: VSRSInference):
        """4. Verify raw and aggregated probability distributions sum to approximately 1.0."""
        dummy_feat = np.random.randn(TOTAL_FEATURE_DIM).astype(np.float32)

        # Frame probability sum
        raw_probs = engine.predict_features_raw(dummy_feat)
        assert np.isclose(np.sum(raw_probs), 1.0, atol=1e-5)

        # Feed 5 frames to obtain aggregated result
        for _ in range(5):
            res = engine.process_frame(dummy_feat)
        assert res.frames_used == 5
        agg_sum = sum(res.class_probabilities.values())
        assert np.isclose(agg_sum, 1.0, atol=1e-4)

    def test_no_prediction_before_5_valid_frames(self, engine: VSRSInference):
        """5. Verify predictions are NOT emitted while buffer has < 5 frames."""
        dummy_feat = np.random.randn(TOTAL_FEATURE_DIM).astype(np.float32)

        for frame_idx in range(1, 5):  # Frames 1..4
            res = engine.process_frame(dummy_feat)
            assert isinstance(res, VSRSInferenceResult)
            assert res.is_accepted is False
            assert res.status == "accumulating_buffer"
            assert res.predicted_label is None
            assert res.confidence == 0.0
            assert res.frames_used == frame_idx
            assert res.class_probabilities == {}

    def test_correct_mean_aggregation_over_5_frames(self):
        """6. Verify temporal aggregation computes the exact arithmetic mean of 5 probability vectors."""
        # Setup mock inference engine with controlled probability outputs
        inf = VSRSInference.__new__(VSRSInference)
        inf.min_confidence = 0.50
        inf.buffer_size = 5
        inf.classes = list(SUPPORTED_VSRS_CLASSES)
        inf.is_loaded = True
        inf._buffer = deque(maxlen=5)
        inf.preprocessor = VSRSPreprocessor()

        # 5 distinct synthetic probability vectors
        prob_matrix = np.zeros((5, 11), dtype=np.float32)
        for i in range(5):
            prob_matrix[i, i] = 0.8  # Dominant class i
            prob_matrix[i, :] += 0.2 / 11
            prob_matrix[i] /= np.sum(prob_matrix[i])

        expected_mean = np.mean(prob_matrix, axis=0)
        expected_top_idx = int(np.argmax(expected_mean))
        expected_top_label = inf.classes[expected_top_idx]
        expected_top_conf = float(expected_mean[expected_top_idx])

        call_idx = [0]
        def mock_predict(feat):
            idx = call_idx[0]
            call_idx[0] += 1
            return prob_matrix[idx]
        inf.predict_features_raw = mock_predict

        dummy_feat = np.zeros(TOTAL_FEATURE_DIM, dtype=np.float32)
        for _ in range(4):
            inf.process_frame(dummy_feat)

        final_res = inf.process_frame(dummy_feat)
        assert final_res.frames_used == 5
        assert final_res.predicted_label == expected_top_label
        assert np.isclose(final_res.confidence, expected_top_conf, atol=1e-5)

        for idx, cls_name in enumerate(inf.classes):
            np.testing.assert_allclose(final_res.class_probabilities[cls_name], expected_mean[idx], atol=1e-5)

    def test_confidence_threshold_acceptance_and_rejection(self):
        """7. Verify confidence >= min_confidence is accepted; below is rejected."""
        inf = VSRSInference.__new__(VSRSInference)
        inf.min_confidence = 0.65
        inf.buffer_size = 5
        inf.classes = list(SUPPORTED_VSRS_CLASSES)
        inf.is_loaded = True
        inf._buffer = deque(maxlen=5)
        inf.preprocessor = VSRSPreprocessor()

        # Case A: Low confidence (flat distribution: 1/11 ~ 0.091 < 0.65)
        flat_probs = np.full(11, 1.0 / 11.0, dtype=np.float32)
        inf.predict_features_raw = lambda feat: flat_probs

        dummy_feat = np.zeros(TOTAL_FEATURE_DIM, dtype=np.float32)
        for _ in range(5):
            res_low = inf.process_frame(dummy_feat)

        assert res_low.frames_used == 5
        assert res_low.is_accepted is False
        assert res_low.status == "low_confidence"
        assert res_low.confidence < 0.65

        # Case B: High confidence (dominant class: 0.90 >= 0.65)
        high_probs = np.zeros(11, dtype=np.float32)
        high_probs[2] = 0.90  # "hello"
        high_probs += 0.10 / 11
        high_probs /= np.sum(high_probs)
        inf.predict_features_raw = lambda feat: high_probs

        inf.reset()
        for _ in range(5):
            res_high = inf.process_frame(dummy_feat)

        assert res_high.frames_used == 5
        assert res_high.is_accepted is True
        assert res_high.status == "success"
        assert res_high.predicted_label == "hello"
        assert res_high.confidence >= 0.65

    def test_buffer_clearing_after_missing_hand(self, engine: VSRSInference):
        """8. Verify buffer is flushed to 0 when preprocessor reports no valid hand."""
        dummy_feat = np.random.randn(TOTAL_FEATURE_DIM).astype(np.float32)

        # Feed 3 valid frames
        for _ in range(3):
            engine.process_frame(dummy_feat)
        assert engine.current_buffer_len == 3

        # Feed frame with no hands (None or empty dict)
        no_hand_res = engine.process_frame(None)
        assert no_hand_res.is_accepted is False
        assert no_hand_res.status == "no_hands_detected"
        assert no_hand_res.frames_used == 0
        assert engine.current_buffer_len == 0

    def test_reset_functionality(self, engine: VSRSInference):
        """9. Verify reset() flushes buffer and allows clean session restart."""
        dummy_feat = np.random.randn(TOTAL_FEATURE_DIM).astype(np.float32)

        for _ in range(4):
            engine.process_frame(dummy_feat)
        assert engine.current_buffer_len == 4

        engine.reset()
        assert engine.current_buffer_len == 0

        # Restart accumulation
        res = engine.process_frame(dummy_feat)
        assert res.frames_used == 1
        assert res.status == "accumulating_buffer"

    def test_invalid_feature_shape_handling(self, engine: VSRSInference):
        """10. Verify passing incorrect feature dimensions raises a ValueError."""
        # Wrong length 1D
        with pytest.raises(ValueError, match="Invalid feature shape"):
            engine.process_frame(np.zeros(100, dtype=np.float32))

        # Wrong length in raw predict
        with pytest.raises(ValueError, match="Invalid feature shape"):
            engine.predict_features_raw(np.zeros(50, dtype=np.float32))

        # 2D matrix with wrong dimensions
        with pytest.raises(ValueError, match="Invalid feature shape"):
            engine.predict_features_raw(np.zeros((2, 100), dtype=np.float32))
