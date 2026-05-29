"""Ruta del Panel de precios (módulo 1)."""
from datetime import date, timedelta

from fastapi import APIRouter, Query

from app.api.deps import XMClientDep
from app.domain.prices import build_price_panel
from app.schemas.prices import PricePanelOut

router = APIRouter(prefix="/prices", tags=["precios"])

METRIC_ID = "PrecBolsNaci"
ENTITY = "Sistema"


def _default_day() -> date:
    """Día por defecto: el día anterior (suele ser el último con dato completo)."""
    return date.today() - timedelta(days=1)


@router.get(
    "",
    response_model=PricePanelOut,
    summary="Precio de bolsa horario y promedio diario",
)
async def get_prices(
    client: XMClientDep,
    day: date = Query(default_factory=_default_day, description="Día a consultar (YYYY-MM-DD)"),
) -> PricePanelOut:
    """Devuelve los 24 valores horarios del precio de bolsa y el promedio diario."""
    records = await client.get_hourly(METRIC_ID, day, day, ENTITY)
    panel = build_price_panel(day, records)
    return PricePanelOut.model_validate(panel)
