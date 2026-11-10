from fastapi import APIRouter
from backend.app.schemas.health import HealthResponse
from backend.app.services.inference_service import inference_service

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def get_health() -> HealthResponse:
    """Return backend health and model readiness status."""
    return HealthResponse(
        status="ok" if inference_service.is_loaded else "degraded",
        model_loaded=inference_service.is_loaded,
        device=inference_service.device_info,
        version="1.0.0",
    )
