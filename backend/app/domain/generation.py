"""Lógica de negocio del Panel de generación (métrica ``Gene``).

Agrupa la generación real horaria por planta dentro de un rango de fechas,
filtra únicamente las plantas de Despacho Central (DC), ordena de mayor a menor
y devuelve el Top N.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.core.exceptions import DataNotFoundError
from app.services.catalog import Catalog
from app.services.xm_client import HourlyRecord

# Gene viene en kWh; se convierte a GWh para una lectura más cómoda.
KWH_TO_GWH = 1_000_000
GENERATION_UNIT = "GWh"
DEFAULT_TOP = 10


@dataclass(frozen=True)
class PlantGeneration:
    """Generación total acumulada de una planta en el rango consultado."""

    code: str
    name: str
    total: float  # en GWh


@dataclass(frozen=True)
class GenerationPanel:
    """Top de plantas de Despacho Central por generación."""

    start: date
    end: date
    unit: str
    plants: list[PlantGeneration]


def build_generation_top(
    start: date,
    end: date,
    records: list[HourlyRecord],
    catalog: Catalog,
    limit: int = DEFAULT_TOP,
) -> GenerationPanel:
    """Construye el Top N de plantas DC por generación total.

    :param records: registros horarios de Gene por Recurso.
    :param catalog: catálogo para filtrar plantas DC y resolver nombres.
    :raises DataNotFoundError: si no hay generación de plantas DC en el rango.
    """
    totals_kwh = _aggregate_dc_generation(records, catalog)
    if not totals_kwh:
        raise DataNotFoundError(
            "No hay generación de plantas de Despacho Central para el rango "
            "seleccionado."
        )

    ranked = sorted(totals_kwh.items(), key=lambda item: item[1], reverse=True)

    plants = [
        PlantGeneration(
            code=code,
            name=catalog.resource_name(code),
            total=round(total_kwh / KWH_TO_GWH, 2),
        )
        for code, total_kwh in ranked[:limit]
    ]

    return GenerationPanel(start=start, end=end, unit=GENERATION_UNIT, plants=plants)


def _aggregate_dc_generation(
    records: list[HourlyRecord], catalog: Catalog
) -> dict[str, float]:
    """Suma la generación horaria por planta, considerando solo plantas DC."""
    totals: dict[str, float] = {}
    for record in records:
        if not catalog.is_centrally_dispatched(record.code):
            continue
        day_total = sum(value for value in record.hours if value is not None)
        totals[record.code] = totals.get(record.code, 0.0) + day_total
    return totals
