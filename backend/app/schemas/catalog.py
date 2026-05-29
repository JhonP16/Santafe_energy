"""Modelos de respuesta para los endpoints de catálogo."""
from pydantic import BaseModel


class AgentOut(BaseModel):
    """Agente expuesto al frontend (para selectores y filtros)."""

    code: str
    name: str
