"""Ruta del Panel de demanda (módulo 3)."""
from datetime import date, timedelta

from fastapi import APIRouter, Query

from app.api.deps import CatalogDep, XMClientDep
from app.domain.demand import build_demand_curve
from app.schemas.demand import DemandPanelOut

router = APIRouter(prefix="/demand", tags=["demanda"])

METRIC_ID = "DemaCome"
ENTITY = "Agente"


def _default_end() -> date:
    return date.today() - timedelta(days=1)


def _default_start() -> date:
    # Periodo de un mes (la API limita a 30 días por consulta horaria).
    return date.today() - timedelta(days=30)


@router.get(
    "",
    response_model=DemandPanelOut,
    summary="Curva de demanda horaria de un agente comercializador",
)
async def get_demand(
    client: XMClientDep,
    catalog: CatalogDep,
    agent: str = Query(..., min_length=1, description="Código SIC del agente comercializador"),
    start: date = Query(default_factory=_default_start, description="Fecha inicial (YYYY-MM-DD)"),
    end: date = Query(default_factory=_default_end, description="Fecha final (YYYY-MM-DD)"),
) -> DemandPanelOut:
    """Devuelve la curva de demanda horaria del agente en el periodo dado."""
    records = await client.get_hourly(METRIC_ID, start, end, ENTITY, filters=[agent])
    panel = build_demand_curve(agent, start, end, records, catalog)
    return DemandPanelOut.model_validate(panel)
