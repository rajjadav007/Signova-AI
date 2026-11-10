"""
API routes for Isolated Indian Sign Language Recognition.
Supports both uploaded video files and direct client landmark sequence arrays.
"""

import logging
from pathlib import Path
from typing import List, Optional

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from backend.app.schemas.isolated import (
    IsolatedRecognitionResponse,
    LandmarkSequenceRequest,
    TopPrediction,
)
from backend.app.services.isolated_inference_service import isolated_inference_service

logger = logging.getLogger("signova.routes.isolated")

router = APIRouter(prefix="/recognize/isolated", tags=["isolated_recognition"])

ALLOWED_VIDEO_EXTENSIONS = {".mp4", ".webm", ".avi", ".mov", ".mkv"}
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB


@router.post("", response_model=IsolatedRecognitionResponse)
@router.post("/landmarks", response_model=IsolatedRecognitionResponse)
def recognize_landmarks(
    request: LandmarkSequenceRequest,
) -> IsolatedRecognitionResponse:
    """
    Recognize an isolated ISL sign from a temporal sequence of MediaPipe landmarks.
    Expected landmark shape: (T, 282) or (T, 376).
    """
    if len(request.landmarks) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Landmark sequence is empty.",
        )

    try:
        raw_result = isolated_inference_service.predict_landmarks(
            raw_keypoints=request.landmarks,
            category=request.category,
            top_k=request.top_k,
        )
    except Exception as exc:
        logger.error("Landmark isolated recognition failure: %s", exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference execution failed: {str(exc)}",
        )

    return IsolatedRecognitionResponse(
        success=raw_result["success"],
        predicted_sign=raw_result["predicted_sign"],
        display_name=raw_result["display_name"],
        category=raw_result["category"],
        confidence=raw_result["confidence"],
        status=raw_result["status"],
        is_valid=raw_result["is_valid"],
        processing_time_ms=raw_result["processing_time_ms"],
        model_used=raw_result["model_used"],
        top_predictions=[TopPrediction(**p) for p in raw_result["top_predictions"]],
        reason=raw_result.get("reason"),
    )


@router.post("/video", response_model=IsolatedRecognitionResponse)
def recognize_video(
    video: UploadFile = File(..., description="Uploaded video file (.mp4, .webm, .avi, .mov, .mkv)"),
    category: Optional[str] = Query(None, description="Optional category filter: alphabet, number, daily, public"),
    top_k: int = Query(3, ge=1, le=10, description="Number of top candidates to return"),
) -> IsolatedRecognitionResponse:
    """
    Process an uploaded video through MediaPipe Holistic landmark extraction and isolated sign classification.
    """
    filename = video.filename or "input.mp4"
    suffix = Path(filename).suffix.lower()

    if suffix not in ALLOWED_VIDEO_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported video format '{suffix}'. Allowed: {sorted(ALLOWED_VIDEO_EXTENSIONS)}",
        )

    try:
        video_bytes = video.file.read()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to read uploaded video stream: {exc}",
        )

    if len(video_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded video file is empty.",
        )

    if len(video_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds {MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB limit.",
        )

    try:
        raw_result = isolated_inference_service.predict_video_file(
            video_bytes=video_bytes,
            filename=filename,
            category=category,
            top_k=top_k,
        )
    except Exception as exc:
        logger.error("Video isolated recognition failure for '%s': %s", filename, exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference execution failed: {str(exc)}",
        )

    return IsolatedRecognitionResponse(
        success=raw_result["success"],
        predicted_sign=raw_result["predicted_sign"],
        display_name=raw_result["display_name"],
        category=raw_result["category"],
        confidence=raw_result["confidence"],
        status=raw_result["status"],
        is_valid=raw_result["is_valid"],
        processing_time_ms=raw_result["processing_time_ms"],
        model_used=raw_result["model_used"],
        top_predictions=[TopPrediction(**p) for p in raw_result["top_predictions"]],
        reason=raw_result.get("reason"),
    )
