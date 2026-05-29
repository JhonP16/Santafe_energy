"""Ruta del Panel de volumen útil (módulo 4)."""
from datetime import date, timedelta

from fastapi import APIRouter

from app.api.deps import XMClientDep
from app.domain.reservoirs import build_reservoir_panel
from app.schemas.reservoirs import ReservoirPanelOut

router = APIRouter(prefix="/reservoirs", tags=["volumen-util"])

METRIC_ID = "PorcVoluUtilDiar"
ENTITY = "Embalse"

# Ventana de consulta para garantizar capturar el último día publicado
# (la métrica diaria puede tener algunos días de rezago).
LOOKBACK_DAYS = 15


@router.get(
    "",
    response_model=ReservoirPanelOut,
    summary="Volumen útil (%) de embalses en el último día registrado",
)
async def get_reservoirs(client: XMClientDep) -> ReservoirPanelOut:
    """Devuelve el volumen útil de los embalses del último día con datos."""
    end = date.today()
    start = end - timedelta(days=LOOKBACK_DAYS)
    records = await client.get_daily(METRIC_ID, start, end, ENTITY)
    panel = build_reservoir_panel(records)
    return ReservoirPanelOut.model_validate(panel)
