"""Rutas de catálogo: listados usados por los filtros del frontend."""
from fastapi import APIRouter

from app.api.deps import CatalogDep
from app.schemas.catalog import AgentOut

router = APIRouter(prefix="/catalog", tags=["catalog"])


@router.get(
    "/comercializadores",
    response_model=list[AgentOut],
    summary="Lista de agentes comercializadores",
)
async def list_marketers(catalog: CatalogDep) -> list[AgentOut]:
    """Devuelve los agentes comercializadores para el panel de demanda."""
    return [AgentOut(code=agent.code, name=agent.name) for agent in catalog.marketers()]
