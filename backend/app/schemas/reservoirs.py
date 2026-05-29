"""Modelos de respuesta del Panel de volumen útil."""
from datetime import date

from pydantic import BaseModel, ConfigDict


class ReservoirOut(BaseModel):
    """Estado de volumen útil de un embalse."""

    model_config = ConfigDict(from_attributes=True)

    name: str
    volume: float
    is_critical: bool


class ReservoirPanelOut(BaseModel):
    """Respuesta de la tabla de volumen útil de embalses."""

    model_config = ConfigDict(from_attributes=True)

    date: date
    unit: str
    threshold: float
    reservoirs: list[ReservoirOut]
