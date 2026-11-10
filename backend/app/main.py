from contextlib import asynccontextmanager
import logging
import os
import sys

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.routes import health, isolated_recognition, predict
from backend.app.core.config import settings
from backend.app.services.inference_service import inference_service
from backend.app.services.isolated_inference_service import isolated_inference_service

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
)
logger = logging.getLogger("signova.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application startup and shutdown lifecycle."""
    if os.getenv("TESTING", "false").lower() == "true":
        yield
        return

    logger.info("Initializing %s...", settings.PROJECT_NAME)
    try:
        inference_service.load_model()
        logger.info("ISLiM model pipeline ready for inference.")
    except Exception as exc:
        logger.error("Failed to load ISLiM model during startup: %s", exc, exc_info=True)

    try:
        isolated_inference_service.load_model()
        logger.info("Isolated sign recognition pipeline ready for inference.")
    except Exception as exc:
        logger.error("Failed to load isolated recognition model during startup: %s", exc, exc_info=True)
    yield
    logger.info("Shutting down %s...", settings.PROJECT_NAME)


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="Signova AI Backend: Indian Sign Language (ISL) recognition API powered by ISLiM.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root-level health check
app.include_router(health.router)

# Versioned API routes (/api/v1/...)
app.include_router(health.router, prefix=settings.API_V1_STR)
app.include_router(predict.router, prefix=settings.API_V1_STR)
app.include_router(isolated_recognition.router, prefix=settings.API_V1_STR)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=False,
    )
