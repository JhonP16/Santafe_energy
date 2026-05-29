"""Cliente HTTP de bajo nivel para la API pública de XM.

Encapsula las peticiones ``POST`` a los endpoints ``/hourly`` y ``/daily`` y
normaliza las respuestas (cuyo formato es bastante anidado) en estructuras
sencillas y tipadas que el resto de la aplicación puede consumir con facilidad.

Formato de la respuesta de XM (resumido)::

    {
      "Items": [
        {
          "Date": "2024-01-15",
          "HourlyEntities": [
            {"Values": {"code": "XXXX", "Hour01": "10.5", ... "Hour24": "9.1"}}
          ]
        }
      ]
    }

Para datos diarios, cada item trae ``DailyEntities`` con ``Name`` y ``Value``.
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date

import httpx

from app.core.exceptions import XMApiError

# La API de XM limita las consultas horarias y diarias a 30 días por petición.
MAX_RANGE_DAYS = 30
HOURS_PER_DAY = 24


@dataclass(frozen=True)
class HourlyRecord:
    """Una serie horaria (24 valores) para una entidad en una fecha."""

    date: date
    code: str
    hours: list[float | None]


@dataclass(frozen=True)
class DailyRecord:
    """Un valor diario para una entidad en una fecha."""

    date: date
    code: str
    value: float | None


def _to_float(raw: object) -> float | None:
    """Convierte un valor de la API a float, tolerando vacíos o no numéricos."""
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


class XMClient:
    """Cliente asíncrono para consumir la API de XM.

    Recibe un ``httpx.AsyncClient`` ya construido (inyección de dependencias),
    lo que facilita reutilizar conexiones y escribir pruebas.
    """

    def __init__(self, client: httpx.AsyncClient, base_url: str) -> None:
        self._client = client
        self._base_url = base_url.rstrip("/")

    async def get_hourly(
        self,
        metric_id: str,
        start: date,
        end: date,
        entity: str,
        filters: list[str] | None = None,
    ) -> list[HourlyRecord]:
        """Consulta una métrica horaria y devuelve registros normalizados."""
        data = await self._post("/hourly", metric_id, start, end, entity, filters)
        return list(self._parse_hourly(data))

    async def get_daily(
        self,
        metric_id: str,
        start: date,
        end: date,
        entity: str,
        filters: list[str] | None = None,
    ) -> list[DailyRecord]:
        """Consulta una métrica diaria y devuelve registros normalizados."""
        data = await self._post("/daily", metric_id, start, end, entity, filters)
        return list(self._parse_daily(data))

    # ----------------------------------------------------------------- interno

    async def _post(
        self,
        endpoint: str,
        metric_id: str,
        start: date,
        end: date,
        entity: str,
        filters: list[str] | None,
    ) -> dict:
        """Ejecuta la petición POST y traduce cualquier fallo a ``XMApiError``."""
        self._validate_range(start, end)

        payload: dict[str, object] = {
            "MetricId": metric_id,
            "StartDate": start.isoformat(),
            "EndDate": end.isoformat(),
            "Entity": entity,
        }
        if filters:
            payload["Filter"] = filters

        try:
            response = await self._client.post(
                f"{self._base_url}{endpoint}", json=payload
            )
            response.raise_for_status()
            return response.json()
        except httpx.TimeoutException as exc:
            raise XMApiError(
                "La API de XM tardó demasiado en responder. Intenta nuevamente."
            ) from exc
        except httpx.HTTPStatusError as exc:
            raise XMApiError(
                f"La API de XM respondió con un error ({exc.response.status_code})."
            ) from exc
        except httpx.HTTPError as exc:
            raise XMApiError(
                "No fue posible conectar con la API de XM."
            ) from exc
        except ValueError as exc:  # JSON inválido
            raise XMApiError(
                "La API de XM devolvió una respuesta no válida."
            ) from exc

    @staticmethod
    def _validate_range(start: date, end: date) -> None:
        """Valida el rango de fechas según las restricciones de la API."""
        if start > end:
            raise XMApiError(
                "La fecha inicial no puede ser posterior a la fecha final.",
                status_code=400,
            )
        if (end - start).days > MAX_RANGE_DAYS:
            raise XMApiError(
                f"El rango máximo permitido por la API de XM es de "
                f"{MAX_RANGE_DAYS} días.",
                status_code=400,
            )

    @staticmethod
    def _parse_hourly(data: dict):
        """Convierte la respuesta cruda horaria en ``HourlyRecord``."""
        for item in data.get("Items") or []:
            item_date = _parse_date(item.get("Date"))
            for entity in item.get("HourlyEntities") or []:
                values = entity.get("Values") or {}
                code = values.get("code") or entity.get("Name") or entity.get("Id")
                hours = [
                    _to_float(values.get(f"Hour{hour:02d}"))
                    for hour in range(1, HOURS_PER_DAY + 1)
                ]
                yield HourlyRecord(date=item_date, code=code, hours=hours)

    @staticmethod
    def _parse_daily(data: dict):
        """Convierte la respuesta cruda diaria en ``DailyRecord``."""
        for item in data.get("Items") or []:
            item_date = _parse_date(item.get("Date"))
            for entity in item.get("DailyEntities") or []:
                values = entity.get("Values") or {}
                code = (
                    values.get("code")
                    or entity.get("Name")
                    or entity.get("Id")
                )
                value = _to_float(
                    entity.get("Value") if "Value" in entity else values.get("Value")
                )
                yield DailyRecord(date=item_date, code=code, value=value)


def _parse_date(raw: str | None) -> date | None:
    """Parsea una fecha 'YYYY-MM-DD' (ignora la parte de hora si existe)."""
    if not raw:
        return None
    return date.fromisoformat(raw[:10])
