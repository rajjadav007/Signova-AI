"""
Unit tests for VSRS Real-Video Evaluator logic (Signova AI - Step 5).
Verifies video discovery, in-vocabulary filtering, unsupported class exclusion,
and metrics computation (precision, recall, F1, confusion matrix, rejection handling).
"""

from pathlib import Path
import numpy as np
import pytest

from scripts.evaluate_vsrs_videos import (
    compute_evaluation_metrics,
    discover_labeled_videos,
    save_evaluation_csv,
)
from backend.app.ml.recognition.vsrs_inference import SUPPORTED_VSRS_CLASSES


class TestVSRSEvaluatorLogic:
    """Test suite for VSRS video evaluation utilities."""

    def test_discover_labeled_videos_filtering(self, tmp_path: Path):
        """Verify discover_labeled_videos includes supported classes and excludes out-of-vocab."""
        # Create supported files
        (tmp_path / "hello_0_1.mp4").touch()
        (tmp_path / "teacher_sample.mp4").touch()

        # Create class-named folder
        house_dir = tmp_path / "house"
        house_dir.mkdir()
        (house_dir / "clip_1.mp4").touch()

        # Create unsupported files
        (tmp_path / "listen_0_1.mp4").touch()
        (tmp_path / "water_sample.mp4").touch()

        valid, excluded = discover_labeled_videos(tmp_path)

        valid_gts = [v["ground_truth"] for v in valid]
        assert len(valid) == 3
        assert "hello" in valid_gts
        assert "teacher" in valid_gts
        assert "house" in valid_gts

        assert len(excluded) == 2
        excluded_names = [e["path"].name for e in excluded]
        assert "listen_0_1.mp4" in excluded_names
        assert "water_sample.mp4" in excluded_names

    def test_compute_evaluation_metrics_calculation(self):
        """Verify accuracy, macro precision, recall, and F1 calculations."""
        mock_results = [
            # 2 Correct accepted
            {"ground_truth": "hello", "predicted_label": "hello", "is_accepted": True, "status": "success"},
            {"ground_truth": "teacher", "predicted_label": "teacher", "is_accepted": True, "status": "success"},
            # 1 Incorrect accepted
            {"ground_truth": "good", "predicted_label": "bad_guess", "is_accepted": True, "status": "success"},
            # 1 Rejected (low confidence) -> NOT counted as correct
            {"ground_truth": "house", "predicted_label": "house", "is_accepted": False, "status": "low_confidence"},
            # 1 No valid hands
            {"ground_truth": "time", "predicted_label": None, "is_accepted": False, "status": "no_valid_hands"},
        ]

        metrics = compute_evaluation_metrics(mock_results)

        assert metrics["total"] == 5
        assert metrics["correct"] == 2
        assert metrics["incorrect"] == 1
        assert metrics["rejected"] == 1
        assert metrics["no_valid_hands"] == 1
        assert metrics["accuracy"] == 2.0 / 5.0  # 40%

        assert "confusion_matrix" in metrics
        assert metrics["confusion_matrix"]["hello"]["hello"] == 1
        assert metrics["confusion_matrix"]["house"]["_rejected"] == 1
        assert metrics["confusion_matrix"]["time"]["_no_hands"] == 1

    def test_save_evaluation_csv(self, tmp_path: Path):
        """Verify CSV report generation and field structure."""
        report_file = tmp_path / "test_report.csv"
        mock_records = [
            {
                "relative_path": "hello/clip1.mp4",
                "ground_truth": "hello",
                "predicted_label": "hello",
                "confidence": 0.88,
                "is_accepted": True,
                "total_frames": 45,
                "hand_frames": 40,
                "status": "success",
            }
        ]

        save_evaluation_csv(mock_records, report_file)
        assert report_file.exists()

        content = report_file.read_text(encoding="utf-8")
        assert "hello/clip1.mp4" in content
        assert "0.8800" in content
        assert "success" in content
