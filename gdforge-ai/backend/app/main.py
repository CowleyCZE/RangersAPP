"""Hlavní aplikace"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import FileResponse
import os

from app.core.config import settings
from app.api import router


def create_app() -> FastAPI:
    """Vytvoří a konfiguruje FastAPI aplikaci"""

    app = FastAPI(
        title=settings.app_title,
        version=settings.app_version,
        description=settings.app_description,
        debug=settings.debug
    )

    # Trusted host middleware - musí být přidáno jako POSLEDNÍ (první v pořadí přidávání)
    app.add_middleware(
        TrustedHostMiddleware,
        allowed_hosts=["*"]  # Povolíme všechny hostitele pro testování
    )

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include API routes
    app.include_router(router, prefix="/api")

    # Root endpoint
    @app.get("/")
    async def root():
        """Root endpoint"""
        return {
            "name": settings.app_title,
            "version": settings.app_version,
            "docs": "/docs",
            "api": "/api/health"
        }

    return app


app = create_app()
