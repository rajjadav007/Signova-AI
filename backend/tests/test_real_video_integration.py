from pathlib import Path
from fastapi.testclient import TestClient
import pytest

from backend.app.main import app
from backend.app.services.inference_service import inference_service

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SAMPLE_VIDEO = PROJECT_ROOT / "vidssavecom-president-prime-minister-chief-minister-indian-sign-language-i_KWDwb1ih.mp4"


@pytest.mark.integration
def test_real_video_prediction_e2e():
    """End-to-end integration test with real ISLiM model and sample video."""
    assert SAMPLE_VIDEO.exists(), f"Sample video not found at {SAMPLE_VIDEO}"

    # Load model once
    inference_service.load_model()
    assert inference_service.is_loaded is True

    with TestClient(app) as client:
        # Check health
        health_resp = client.get("/api/v1/health")
        assert health_resp.status_code == 200
        health_data = health_resp.json()
        assert health_data["model_loaded"] is True

        # Send real video for prediction
        with open(SAMPLE_VIDEO, "rb") as f:
            video_bytes = f.read()

        files = {"video": (SAMPLE_VIDEO.name, video_bytes, "video/mp4")}
        pred_resp = client.post("/api/v1/predict/video?decoding=beam", files=files)

        assert pred_resp.status_code == 200, f"Error: {pred_resp.text}"
        data = pred_resp.json()

        assert data["success"] is True
        assert isinstance(data["predicted_text"], str)
        assert len(data["predicted_text"].strip()) > 0
        assert data["decoding"] == "beam"
        assert data["inference_time_seconds"] > 0
        print(f"\n[Real Video E2E Result] Prediction: '{data['predicted_text']}' in {data['inference_time_seconds']}s")
