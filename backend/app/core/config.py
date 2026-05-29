"""Configuración central de la aplicación.

Carga los parámetros desde variables de entorno (o un archivo ``.env``) usando
pydantic-settings, de modo que el resto del código nunca lea ``os.environ``
directamente.
"""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

# Raíz del repositorio: .../backend/app/core/config.py -> sube 3 niveles.
BACKEND_DIR = Path(__file__).resolve().parents[2]
PROJECT_ROOT = BACKEND_DIR.parent


class Settings(BaseSettings):
    """Parámetros de configuración de la aplicación."""

    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- API de XM ---
    xm_api_base_url: str = "https://servapibi.xm.com.co"
    xm_api_timeout: float = 60.0

    # --- CORS ---
    cors_origins: str = "http://localhost:5173,http://127.0.0.1:5173"

    # --- Catálogos (archivos Excel provistos en el reto) ---
    recursos_xlsx: Path = PROJECT_ROOT / "recursos.xlsx"
    agentes_xlsx: Path = PROJECT_ROOT / "agentes.xlsx"

    @property
    def cors_origins_list(self) -> list[str]:
        """Lista de orígenes permitidos a partir de la cadena separada por comas."""
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


@lru_cache
def get_settings() -> Settings:
    """Devuelve una instancia única (cacheada) de la configuración."""
    return Settings()
