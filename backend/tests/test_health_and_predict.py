import io
import os
os.environ["TESTING"] = "true"
from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient
import pytest

from backend.app.main import app
from backend.app.services.inference_service import inference_service


@pytest.fixture
def client():
    # Use TestClient with lifespan load_model mocked for instant unit testing
    with patch("backend.app.main.inference_service.load_model"):
        with TestClient(app, raise_server_exceptions=False) as c:
            yield c


def test_health_endpoint_unloaded(client):
    """Test health endpoint reports degraded status when model is not loaded."""
    with patch.object(inference_service, "is_loaded", False), \
         patch.object(inference_service, "device_info", "uninitialized"):
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "degraded"
        assert data["model_loaded"] is False


def test_health_endpoint_loaded(client):
    """Test health endpoint reports ok status when model is loaded."""
    with patch.object(inference_service, "is_loaded", True), \
         patch.object(inference_service, "device_info", "cuda:0"):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["model_loaded"] is True
        assert data["device"] == "cuda:0"


def test_predict_video_model_unready(client):
    """Test predict endpoint returns 503 when model is not loaded."""
    with patch.object(inference_service, "is_loaded", False):
        files = {"video": ("sample.mp4", b"dummy video bytes", "video/mp4")}
        response = client.post("/api/v1/predict/video", files=files)
        assert response.status_code == 503
        assert "not loaded" in response.json()["detail"]


def test_predict_video_invalid_extension(client):
    """Test predict endpoint rejects unsupported file formats with 400."""
    with patch.object(inference_service, "is_loaded", True):
        files = {"video": ("sample.txt", b"dummy text", "text/plain")}
        response = client.post("/api/v1/predict/video", files=files)
        assert response.status_code == 400
        assert "Unsupported video format" in response.json()["detail"]


def test_predict_video_empty_file(client):
    """Test predict endpoint rejects empty video files with 400."""
    with patch.object(inference_service, "is_loaded", True):
        files = {"video": ("empty.mp4", b"", "video/mp4")}
        response = client.post("/api/v1/predict/video", files=files)
        assert response.status_code == 400
        assert "empty" in response.json()["detail"]


def test_predict_video_mock_success(client):
    """Test predict endpoint successfully returns prediction on valid input."""
    mock_result = {
        "prediction": "PRESIDENT PRIME MINISTER",
        "timings": {
            "total_processing_time_seconds": 1.45,
        },
        "device": {
            "name": "NVIDIA GeForce RTX",
        },
    }

    with patch.object(inference_service, "is_loaded", True), \
         patch.object(inference_service, "device_info", "cuda:0"), \
         patch.object(inference_service, "predict_video_file", return_value=mock_result):
        
        files = {"video": ("test.mp4", b"valid mock video content", "video/mp4")}
        response = client.post("/api/v1/predict/video?decoding=beam", files=files)
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["predicted_text"] == "PRESIDENT PRIME MINISTER"
        assert data["decoding"] == "beam"
        assert data["inference_time_seconds"] == 1.45
        assert data["video_name"] == "test.mp4"
