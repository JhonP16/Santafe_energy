"""Excepciones de dominio y manejadores globales de errores.

Centralizar el manejo de errores garantiza que el frontend siempre reciba una
respuesta JSON consistente y un mensaje claro, incluso cuando la API de XM
falla o no devuelve datos.
"""
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


class AppError(Exception):
    """Error base de la aplicación con mensaje amigable y código HTTP."""

    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self, message: str, status_code: int | None = None) -> None:
        super().__init__(message)
        self.message = message
        if status_code is not None:
            self.status_code = status_code


class XMApiError(AppError):
    """La API de XM devolvió un error o no se pudo contactar."""

    status_code = status.HTTP_502_BAD_GATEWAY


class DataNotFoundError(AppError):
    """La consulta fue válida pero no hay datos para los parámetros dados."""

    status_code = status.HTTP_404_NOT_FOUND


def register_exception_handlers(app: FastAPI) -> None:
    """Registra los manejadores que convierten excepciones en respuestas JSON."""

    @app.exception_handler(AppError)
    async def _handle_app_error(_: Request, exc: AppError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message},
        )
