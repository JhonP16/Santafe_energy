"""Lógica de negocio del Panel de demanda (métrica ``DemaCome``).

Construye la curva de demanda comercial horaria de un agente comercializador a
lo largo de un periodo (hasta 1 mes), aplanando los valores horarios en una
serie temporal lista para graficar.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.core.exceptions import DataNotFoundError
from app.services.catalog import Catalog
from app.services.xm_client import HourlyRecord

# DemaCome viene en kWh.
DEMAND_UNIT = "kWh"


@dataclass(frozen=True)
class DemandPoint:
    """Un punto de la curva: instante (fecha + hora) y demanda en ese instante."""

    timestamp: str  # ISO 'YYYY-MM-DDTHH:00'
    value: float | None


@dataclass(frozen=True)
class DemandPanel:
    """Curva de demanda horaria de un agente comercializador."""

    agent_code: str
    agent_name: str
    start: date
    end: date
    unit: str
    average: float | None
    points: list[DemandPoint]


def build_demand_curve(
    agent_code: str,
    start: date,
    end: date,
    records: list[HourlyRecord],
    catalog: Catalog,
) -> DemandPanel:
    """Construye la curva de demanda horaria del agente en el periodo.

    :param records: registros horarios de DemaCome filtrados por el agente.
    :raises DataNotFoundError: si no hay datos de demanda para el agente/periodo.
    """
    points = _to_time_series(records)
    if not points:
        raise DataNotFoundError(
            "No hay datos de demanda para el agente y periodo seleccionados."
        )

    measured = [p.value for p in points if p.value is not None]
    average = round(sum(measured) / len(measured), 2) if measured else None

    return DemandPanel(
        agent_code=agent_code,
        agent_name=catalog.agent_name(agent_code),
        start=start,
        end=end,
        unit=DEMAND_UNIT,
        average=average,
        points=points,
    )


def _to_time_series(records: list[HourlyRecord]) -> list[DemandPoint]:
    """Aplana los registros horarios en una serie temporal ordenada por fecha/hora."""
    points: list[DemandPoint] = []
    for record in sorted(records, key=lambda r: r.date):
        for hour_index, value in enumerate(record.hours):
            timestamp = f"{record.date.isoformat()}T{hour_index:02d}:00"
            points.append(DemandPoint(timestamp=timestamp, value=_round(value)))
    return points


def _round(value: float | None) -> float | None:
    return round(value, 2) if value is not None else None
