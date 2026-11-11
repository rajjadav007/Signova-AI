from fastapi import APIRouter

from app.api.routes import health

api_router = APIRouter()

# Register modular routes
api_router.include_router(health.router)

__all__ = ["api_router"]
