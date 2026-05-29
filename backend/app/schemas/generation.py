"""Modelos de respuesta del Panel de generación."""
from datetime import date

from pydantic import BaseModel, ConfigDict


class PlantGenerationOut(BaseModel):
    """Generación total de una planta."""

    model_config = ConfigDict(from_attributes=True)

    code: str
    name: str
    total: float


class GenerationPanelOut(BaseModel):
    """Respuesta del Top de plantas DC por generación."""

    model_config = ConfigDict(from_attributes=True)

    start: date
    end: date
    unit: str
    plants: list[PlantGenerationOut]
