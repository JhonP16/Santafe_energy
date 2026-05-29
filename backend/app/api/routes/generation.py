"""Ruta del Panel de generación (módulo 2)."""
from datetime import date, timedelta

from fastapi import APIRouter, Query

from app.api.deps import CatalogDep, XMClientDep
from app.domain.generation import DEFAULT_TOP, build_generation_top
from app.schemas.generation import GenerationPanelOut

router = APIRouter(prefix="/generation", tags=["generación"])

METRIC_ID = "Gene"
ENTITY = "Recurso"


def _default_end() -> date:
    return date.today() - timedelta(days=1)


def _default_start() -> date:
    return date.today() - timedelta(days=7)


@router.get(
    "",
    response_model=GenerationPanelOut,
    summary="Top de plantas de Despacho Central por generación",
)
async def get_generation(
    client: XMClientDep,
    catalog: CatalogDep,
    start: date = Query(default_factory=_default_start, description="Fecha inicial (YYYY-MM-DD)"),
    end: date = Query(default_factory=_default_end, description="Fecha final (YYYY-MM-DD)"),
    limit: int = Query(default=DEFAULT_TOP, ge=1, le=50, description="Cantidad de plantas en el ranking"),
) -> GenerationPanelOut:
    """Devuelve las plantas DC con mayor generación total en el rango dado."""
    records = await client.get_hourly(METRIC_ID, start, end, ENTITY)
    panel = build_generation_top(start, end, records, catalog, limit=limit)
    return GenerationPanelOut.model_validate(panel)
