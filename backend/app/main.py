"""Punto de entrada de la aplicación FastAPI.

Crea la app, configura CORS, registra los manejadores de errores y monta el
router principal bajo el prefijo ``/api``.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers


def create_app() -> FastAPI:
    """Construye y configura la instancia de FastAPI (application factory)."""
    settings = get_settings()

    app = FastAPI(
        title="Santafé Energy API",
        description=(
            "Backend que consume la API pública de XM y expone los datos "
            "procesados para los paneles de precios, generación, demanda y "
            "volumen útil de embalses."
        ),
        version="0.1.0",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    register_exception_handlers(app)
    app.include_router(api_router, prefix="/api")

    return app


app = create_app()
