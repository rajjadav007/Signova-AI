try:
    from app.schemas.health import HealthResponse
    from app.schemas.error import ErrorResponse, ErrorDetail
    from app.schemas.predict import PredictionResponse
    from app.schemas.isolated import (
        IsolatedRecognitionResponse,
        LandmarkSequenceRequest,
        TopPrediction,
    )
except ModuleNotFoundError:
    from backend.app.schemas.health import HealthResponse
    from backend.app.schemas.error import ErrorResponse, ErrorDetail
    from backend.app.schemas.predict import PredictionResponse
    from backend.app.schemas.isolated import (
        IsolatedRecognitionResponse,
        LandmarkSequenceRequest,
        TopPrediction,
    )

__all__ = [
    "HealthResponse",
    "ErrorResponse",
    "ErrorDetail",
    "PredictionResponse",
    "IsolatedRecognitionResponse",
    "LandmarkSequenceRequest",
    "TopPrediction",
]
