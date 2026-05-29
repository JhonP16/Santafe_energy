"""Lógica de negocio del Panel de precios (métrica ``PrecBolsNaci``).

A partir de los 24 valores horarios del Precio de Bolsa Nacional de un día,
calcula la información necesaria para el box plot y el Precio de Bolsa
Promedio diario.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.core.exceptions import DataNotFoundError
from app.services.xm_client import HourlyRecord

# Unidad de la métrica PrecBolsNaci.
PRICE_UNIT = "COP/kWh"


@dataclass(frozen=True)
class HourValue:
    """Valor del precio en una hora puntual (1-24)."""

    hour: int
    value: float


@dataclass(frozen=True)
class PricePanel:
    """Datos consolidados del panel de precios para un día."""

    date: date
    unit: str
    average: float
    peak: HourValue
    lowest: HourValue
    values: list[HourValue]


def build_price_panel(day: date, records: list[HourlyRecord]) -> PricePanel:
    """Construye el panel de precios a partir de los registros horarios de XM.

    :param day: día consultado.
    :param records: registros horarios devueltos por la API (entidad Sistema).
    :raises DataNotFoundError: si no hay valores de precio para el día.
    """
    hour_values = _extract_hour_values(records)
    if not hour_values:
        raise DataNotFoundError(
            f"No hay datos de precio de bolsa para el {day.isoformat()}."
        )

    average = sum(hv.value for hv in hour_values) / len(hour_values)

    return PricePanel(
        date=day,
        unit=PRICE_UNIT,
        average=round(average, 2),
        peak=max(hour_values, key=lambda hv: hv.value),
        lowest=min(hour_values, key=lambda hv: hv.value),
        values=hour_values,
    )


def _extract_hour_values(records: list[HourlyRecord]) -> list[HourValue]:
    """Aplana los registros (entidad Sistema) a una lista de (hora, valor).

    Se descartan las horas sin dato. Para PrecBolsNaci por Sistema se espera un
    único registro por día, pero se itera por robustez.
    """
    hour_values: list[HourValue] = []
    for record in records:
        for index, value in enumerate(record.hours, start=1):
            if value is not None:
                hour_values.append(HourValue(hour=index, value=round(value, 2)))
    return hour_values
