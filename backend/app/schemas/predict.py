from typing import Optional
from pydantic import BaseModel


class PredictionResponse(BaseModel):
    success: bool
    predicted_text: str
    decoding: str
    inference_time_seconds: float
    video_name: str
    device: str
    error: Optional[str] = None
