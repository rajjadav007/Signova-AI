import asyncio
import logging
from pathlib import Path
from typing import Literal

from fastapi import APIRouter, File, HTTPException, Query, UploadFile, status

from backend.app.schemas.predict import PredictionResponse
from backend.app.services.inference_service import inference_service

logger = logging.getLogger("signova.routes.predict")

router = APIRouter(prefix="/predict", tags=["prediction"])

ALLOWED_EXTENSIONS = {".mp4", ".webm", ".avi", ".mov", ".mkv"}
MAX_FILE_SIZE_BYTES = 50 * 1024 * 1024  # 50 MB limit


@router.post("/video", response_model=PredictionResponse)
async def predict_video(
    video: UploadFile = File(..., description="Uploaded video file (.mp4, .webm, .avi, .mov, .mkv)"),
    decoding: Literal["beam", "greedy"] = Query("beam", description="T5 text decoding strategy"),
) -> PredictionResponse:
    """
    Process an uploaded video through MediaPipe landmark extraction and ISLiM translation.
    """
    if not inference_service.is_loaded:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="ISLiM model is not loaded or still initializing.",
        )

    filename = video.filename or "input.mp4"
    suffix = Path(filename).suffix.lower()

    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Unsupported video format '{suffix}'. Allowed: {sorted(ALLOWED_EXTENSIONS)}",
        )

    try:
        video_bytes = await video.read()
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

    # Offload heavy synchronous ML inference to worker thread pool
    try:
        raw_result = await asyncio.to_thread(
            inference_service.predict_video_file,
            video_bytes=video_bytes,
            filename=filename,
            decoding=decoding,
        )
    except Exception as exc:
        logger.error("Inference failure for '%s': %s", filename, exc, exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Inference execution failed: {str(exc)}",
        )

    predicted_text = raw_result.get("prediction", "")
    timings = raw_result.get("timings", {})
    duration_sec = timings.get("total_processing_time_seconds", 0.0)
    device_name = raw_result.get("device", {}).get("name", inference_service.device_info)

    return PredictionResponse(
        success=True,
        predicted_text=predicted_text,
        decoding=decoding,
        inference_time_seconds=duration_sec,
        video_name=filename,
        device=device_name,
    )
