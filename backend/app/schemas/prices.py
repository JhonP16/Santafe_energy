"""Modelos de respuesta del Panel de precios."""
from datetime import date

from pydantic import BaseModel, ConfigDict


class HourValueOut(BaseModel):
    """Valor de precio en una hora del día."""

    model_config = ConfigDict(from_attributes=True)

    hour: int
    value: float


class PricePanelOut(BaseModel):
    """Respuesta del panel de precios para un día."""

    model_config = ConfigDict(from_attributes=True)

    date: date
    unit: str
    average: float
    peak: HourValueOut
    lowest: HourValueOut
    values: list[HourValueOut]
