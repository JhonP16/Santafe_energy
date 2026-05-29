"""Punto de entrada de la aplicación FastAPI.

Crea la app, configura CORS, registra los manejadores de errores y monta el
router principal bajo el prefijo ``/api``.
"""
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import api_router
from app.core.config import get_settings
from app.core.exceptions import register_exception_handlers
from app.services.xm_client import XMClient


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Crea recursos compartidos al iniciar y los libera al apagar la app.

    Se mantiene un único ``httpx.AsyncClient`` durante toda la vida de la
    aplicación para reutilizar conexiones hacia la API de XM.
    """
    settings = get_settings()
    async with httpx.AsyncClient(
        timeout=settings.xm_api_timeout,
        headers={"Content-Type": "application/json"},
    ) as http_client:
        app.state.xm_client = XMClient(http_client, settings.xm_api_base_url)
        yield


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
        lifespan=lifespan,
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
