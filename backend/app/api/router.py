"""Router principal que agrupa todas las rutas de la API.

Cada módulo del reto registra aquí su propio router; por ahora solo el health
check, y los demás se irán añadiendo de forma incremental.
"""
from fastapi import APIRouter

from app.api.routes import catalog, demand, generation, health, prices, reservoirs

api_router = APIRouter()
api_router.include_router(health.router)
api_router.include_router(catalog.router)
api_router.include_router(prices.router)
api_router.include_router(generation.router)
api_router.include_router(demand.router)
api_router.include_router(reservoirs.router)
