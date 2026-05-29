"""Lógica de negocio del Panel de volumen útil (métrica ``PorcVoluUtilDiar``).

Toma el último día con dato registrado en la respuesta de XM y arma la tabla de
volumen útil (%) de los embalses, marcando como críticos los que están por
debajo del umbral de alerta.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.core.exceptions import DataNotFoundError
from app.services.xm_client import DailyRecord

# Umbral de alerta: se resalta el embalse si su volumen útil es inferior a este %.
ALERT_THRESHOLD = 30.0
VOLUME_UNIT = "%"


@dataclass(frozen=True)
class Reservoir:
    """Estado del volumen útil de un embalse en un día."""

    name: str
    volume: float  # porcentaje (0-100)
    is_critical: bool


@dataclass(frozen=True)
class ReservoirPanel:
    """Tabla de volumen útil de embalses para el último día registrado."""

    date: date
    unit: str
    threshold: float
    reservoirs: list[Reservoir]


def build_reservoir_panel(
    records: list[DailyRecord], threshold: float = ALERT_THRESHOLD
) -> ReservoirPanel:
    """Construye la tabla de embalses usando el último día con datos.

    :param records: registros diarios de PorcVoluUtilDiar por Embalse.
    :raises DataNotFoundError: si no hay ningún dato de volumen útil.
    """
    valid = [r for r in records if r.date is not None and r.value is not None]
    if not valid:
        raise DataNotFoundError("No hay datos de volumen útil de embalses disponibles.")

    last_date = max(r.date for r in valid)

    reservoirs = [
        _to_reservoir(record, threshold)
        for record in valid
        if record.date == last_date
    ]
    # Orden ascendente: los embalses más críticos quedan primero.
    reservoirs.sort(key=lambda r: r.volume)

    return ReservoirPanel(
        date=last_date,
        unit=VOLUME_UNIT,
        threshold=threshold,
        reservoirs=reservoirs,
    )


def _to_reservoir(record: DailyRecord, threshold: float) -> Reservoir:
    """Convierte un registro diario (fracción 0-1) a porcentaje con su alerta."""
    volume = round(record.value * 100, 1)
    return Reservoir(
        name=record.code,
        volume=volume,
        is_critical=volume < threshold,
    )
