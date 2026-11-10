"""
Pydantic schemas for the Isolated ISL Recognition endpoints.
"""

from typing import List, Optional
from pydantic import BaseModel, Field


class TopPrediction(BaseModel):
    label: str = Field(..., description="ISL gloss label (e.g. 'HELLO', 'A', 'DOCTOR')")
    display_name: str = Field(..., description="User-facing display name")
    confidence: float = Field(..., description="Softmax confidence score [0.0, 1.0]")
    category: str = Field(..., description="Category: 'alphabet', 'number', 'daily', 'public'")


class LandmarkSequenceRequest(BaseModel):
    landmarks: List[List[float]] = Field(
        ...,
        description="Flattened sequence of MediaPipe keypoints: shape (T, 282) or (T, 376)",
    )
    category: Optional[str] = Field(
        None,
        description="Optional filter category: 'alphabet', 'number', 'daily', 'public'",
    )
    top_k: int = Field(3, ge=1, le=10, description="Number of top candidates to return")


class IsolatedRecognitionResponse(BaseModel):
    success: bool = Field(True, description="Whether inference completed successfully")
    predicted_sign: str = Field(..., description="Highest-scoring predicted ISL gloss label")
    display_name: str = Field(..., description="Human-readable sign name")
    category: str = Field(..., description="Class category ('alphabet', 'number', 'daily', 'public')")
    confidence: float = Field(..., description="Prediction confidence [0.0, 1.0]")
    status: str = Field(
        ...,
        description="Recognition status: 'recognized', 'low_confidence', 'poor_tracking', 'incomplete_gesture', 'unknown_sign'",
    )
    is_valid: bool = Field(..., description="True if status == 'recognized'")
    processing_time_ms: float = Field(..., description="End-to-end processing time in milliseconds")
    model_used: str = Field(..., description="Active model architecture name")
    top_predictions: List[TopPrediction] = Field(default_factory=list, description="Top candidate predictions")
    reason: Optional[str] = Field(None, description="Detailed explanation if prediction rejected")
