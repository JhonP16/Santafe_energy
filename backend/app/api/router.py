"""Router principal que agrupa todas las rutas de la API.

Cada módulo del reto registra aquí su propio router; por ahora solo el health
check, y los demás se irán añadiendo de forma incremental.
"""
from fastapi import APIRouter

from app.api.routes import catalog, health

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(catalog.router)
