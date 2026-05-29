"""Modelos de respuesta del Panel de demanda."""
from datetime import date

from pydantic import BaseModel, ConfigDict


class DemandPointOut(BaseModel):
    """Punto de la curva de demanda."""

    model_config = ConfigDict(from_attributes=True)

    timestamp: str
    value: float | None


class DemandPanelOut(BaseModel):
    """Respuesta de la curva de demanda de un agente."""

    model_config = ConfigDict(from_attributes=True)

    agent_code: str
    agent_name: str
    start: date
    end: date
    unit: str
    average: float | None
    points: list[DemandPointOut]
