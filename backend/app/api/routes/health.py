"""Endpoint de health check para verificar que el servicio está activo."""
from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health", summary="Estado del servicio")
async def health() -> dict[str, str]:
    """Devuelve un estado simple para monitoreo y verificación de despliegue."""
    return {"status": "ok"}
