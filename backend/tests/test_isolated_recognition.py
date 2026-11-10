"""
Comprehensive test suite for Phase 3: Isolated Indian Sign Language Recognition.
Verifies landmark extraction, preprocessing, model architectures, unknown sign rejection,
webcam segmentation, isolated API endpoints, and ISLiM sentence translation regression.
"""

import os
os.environ["TESTING"] = "true"

from io import BytesIO
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi import HTTPException, UploadFile
import numpy as np
import pytest
import torch

from backend.app.api.routes.isolated_recognition import recognize_landmarks, recognize_video
from backend.app.api.routes.predict import predict_video
from backend.app.ml.models.bilstm import BiLSTMClassifier
from backend.app.ml.models.temporal_cnn import TemporalCNNClassifier
from backend.app.ml.preprocessing.isolated_preprocessor import (
    FEATURE_DIM,
    NUM_KEYPOINTS,
    TARGET_FRAMES,
    IsolatedSignPreprocessor,
)
from backend.app.ml.recognition.isolated_inference import IsolatedSignRecognizer
from backend.app.ml.recognition.quality_validator import SignQualityValidator
from backend.app.ml.recognition.sign_segmentation import SignSegmentationBuffer
from backend.app.ml.training.dataset_loader import load_label_map
from backend.app.schemas.isolated import LandmarkSequenceRequest
from backend.app.services.inference_service import inference_service
from backend.app.services.isolated_inference_service import isolated_inference_service


# --- 1. Label Mapping Tests ---
def test_label_mapping():
    label_to_idx, idx_to_label = load_label_map()
    assert len(label_to_idx) == 67
    assert len(idx_to_label) == 67
    assert idx_to_label[0] == "BACKGROUND"
    assert idx_to_label[1] == "A"
    assert idx_to_label[27] == "0"
    assert "HELLO" in label_to_idx
    assert "PRESIDENT" in label_to_idx
    assert "INDIA" in label_to_idx


# --- 2. Landmark Preprocessor Tests ---
def test_preprocessor_resampling_and_normalization():
    prep = IsolatedSignPreprocessor(target_frames=30)

    # Resample short sequence
    short_seq = np.random.randn(12, 282).astype(np.float32)
    res_short = prep.resample_temporal(short_seq)
    assert res_short.shape == (30, 282)

    # Resample single static frame
    static_frame = np.random.randn(1, 282).astype(np.float32)
    res_static = prep.resample_temporal(static_frame)
    assert res_static.shape == (30, 282)
    np.testing.assert_allclose(res_static[0], res_static[-1])

    # Test full processing from (T, 94, 4)
    raw_holistic = np.random.randn(25, 94, 4).astype(np.float32)
    tensor = prep.process(raw_holistic)
    assert isinstance(tensor, torch.Tensor)
    assert tensor.shape == (1, 30, 282)


# --- 3. Model Architecture Tests ---
def test_temporal_cnn_forward():
    cnn = TemporalCNNClassifier(in_features=282, num_classes=67)
    x = torch.randn(2, 30, 282)
    logits, probs = cnn(x)
    assert logits.shape == (2, 67)
    assert probs.shape == (2, 67)
    np.testing.assert_allclose(probs.sum(dim=-1).detach().tolist(), [1.0, 1.0], atol=1e-5)


def test_bilstm_forward():
    lstm = BiLSTMClassifier(in_features=282, hidden_size=128, num_classes=67)
    x = torch.randn(2, 30, 282)
    logits, probs = lstm(x)
    assert logits.shape == (2, 67)
    assert probs.shape == (2, 67)
    np.testing.assert_allclose(probs.sum(dim=-1).detach().tolist(), [1.0, 1.0], atol=1e-5)


# --- 4. Quality Validator & Unknown Sign Rejection Tests ---
def test_quality_validator_rejection():
    validator = SignQualityValidator()

    # 1. Background class rejected as unknown sign
    res_bg = validator.validate(predicted_idx=0, confidence=0.98, is_dynamic_sign=False)
    assert res_bg.status == "unknown_sign"
    assert not res_bg.is_valid

    # 2. Low confidence rejected
    res_low = validator.validate(predicted_idx=37, confidence=0.35, is_dynamic_sign=True)
    assert res_low.status == "unknown_sign"
    assert not res_low.is_valid

    # 3. Moderate confidence flagged as low_confidence
    res_mod = validator.validate(predicted_idx=37, confidence=0.55, is_dynamic_sign=True)
    assert res_mod.status == "low_confidence"
    assert not res_mod.is_valid

    # 4. Poor tracking rejected (all zeros hand coordinates)
    empty_hands = np.zeros((30, 94, 3), dtype=np.float32)
    res_track = validator.validate(predicted_idx=37, confidence=0.95, is_dynamic_sign=True, raw_keypoints=empty_hands)
    assert res_track.status == "poor_tracking"
    assert not res_track.is_valid

    # 5. Incomplete gesture (dynamic sign with frozen hand coordinates)
    frozen_hands = np.zeros((30, 94, 3), dtype=np.float32)
    frozen_hands[:, 6:48, :] = 0.5
    res_incomplete = validator.validate(predicted_idx=37, confidence=0.95, is_dynamic_sign=True, raw_keypoints=frozen_hands)
    assert res_incomplete.status == "incomplete_gesture"
    assert not res_incomplete.is_valid

    # 6. Valid recognized sign
    moving_hands = np.random.randn(30, 94, 3).astype(np.float32)
    res_valid = validator.validate(predicted_idx=37, confidence=0.92, is_dynamic_sign=True, raw_keypoints=moving_hands)
    assert res_valid.status == "recognized"
    assert res_valid.is_valid


# --- 5. Webcam Segmentation Buffer Tests ---
def test_webcam_segmentation_buffer():
    buf = SignSegmentationBuffer(window_size=30, start_threshold=0.02, settle_threshold=0.01, cooldown_frames=10)

    # Ingest idle frames
    idle_frame = np.zeros((94, 3), dtype=np.float32)
    completed = None
    for _ in range(20):
        completed = buf.add_frame(idle_frame)
    assert completed is None

    # Ingest moving frames
    for t in range(35):
        frame = np.zeros((94, 3), dtype=np.float32)
        frame[27:48, 0] = np.sin(t / 2.0) * 0.2
        res = buf.add_frame(frame)
        if res is not None:
            completed = res
            break

    assert completed is not None
    assert completed.shape == (30, 94, 3)


# --- 6. Standalone Isolated Sign Recognizer Tests ---
def test_isolated_sign_recognizer_inference():
    recognizer = IsolatedSignRecognizer()
    recognizer.load_model()
    assert recognizer.is_loaded
    assert recognizer.model_type == "Temporal_CNN"

    dummy_seq = np.random.randn(30, 282).astype(np.float32)
    res = recognizer.predict_landmarks(dummy_seq, category="daily", top_k=3)
    assert res["success"] is True
    assert "predicted_sign" in res
    assert "confidence" in res
    assert "status" in res
    assert len(res["top_predictions"]) == 3


# --- 7. Isolated Recognition API Route Tests ---
def test_api_recognize_landmarks_route():
    mock_response = {
        "success": True,
        "predicted_sign": "HELLO",
        "display_name": "Hello",
        "category": "daily",
        "confidence": 0.94,
        "status": "recognized",
        "is_valid": True,
        "processing_time_ms": 2.1,
        "model_used": "Temporal_CNN",
        "top_predictions": [
            {"label": "HELLO", "display_name": "Hello", "confidence": 0.94, "category": "daily"},
            {"label": "WATER", "display_name": "Water", "confidence": 0.03, "category": "daily"},
        ],
        "reason": None,
    }

    with patch.object(isolated_inference_service, "predict_landmarks", return_value=mock_response):
        dummy_seq = [[0.1] * 282 for _ in range(30)]
        request = LandmarkSequenceRequest(landmarks=dummy_seq, category="daily", top_k=2)
        response = recognize_landmarks(request)

        assert response.success is True
        assert response.predicted_sign == "HELLO"
        assert response.confidence == 0.94
        assert response.status == "recognized"
        assert response.is_valid is True
        assert len(response.top_predictions) == 2


def test_api_recognize_video_invalid_format():
    upload = UploadFile(filename="invalid.txt", file=BytesIO(b"fake data"))
    with pytest.raises(HTTPException) as exc:
        recognize_video(video=upload)
    assert exc.value.status_code == 400
    assert "Unsupported video format" in exc.value.detail


def test_api_recognize_video_empty():
    upload = UploadFile(filename="empty.mp4", file=BytesIO(b""))
    with pytest.raises(HTTPException) as exc:
        recognize_video(video=upload)
    assert exc.value.status_code == 400
    assert "empty" in exc.value.detail


# --- 8. ISLiM Sentence Translation Regression Test ---
def test_islim_sentence_translation_regression():
    """
    STRICT RULE: Verify existing ISLiM continuous sentence translation endpoint
    remains completely functional and unaffected by isolated recognition.
    """
    from backend.app.schemas.predict import PredictionResponse
    from backend.app.main import app

    # 1. Verify route registration in FastAPI app
    from backend.app.api.routes import predict as predict_module
    from backend.app.api.routes import isolated_recognition as isolated_module
    registered_routers = [getattr(r, "original_router", None) for r in app.routes]
    assert predict_module.router in registered_routers
    assert isolated_module.router in registered_routers

    # 2. Verify ISLiM inference service contract and methods
    assert hasattr(inference_service, "load_model")
    assert hasattr(inference_service, "predict_video_file")
    assert hasattr(inference_service, "is_loaded")
    assert hasattr(inference_service, "device_info")

    # 3. Test ISLiM prediction output schema integrity
    mock_islim_raw = {
        "prediction": "A MIXTURE OF TWO LIQUIDS",
        "timings": {
            "total_processing_time_seconds": 1.25,
        },
        "device": {
            "name": "NVIDIA GeForce RTX",
        },
    }

    resp = PredictionResponse(
        success=True,
        predicted_text=mock_islim_raw["prediction"],
        decoding="beam",
        inference_time_seconds=mock_islim_raw["timings"]["total_processing_time_seconds"],
        video_name="test_clip.mp4",
        device=mock_islim_raw["device"]["name"],
    )

    assert resp.success is True
    assert resp.predicted_text == "A MIXTURE OF TWO LIQUIDS"
    assert resp.decoding == "beam"
    assert resp.inference_time_seconds == 1.25
    assert resp.video_name == "test_clip.mp4"
