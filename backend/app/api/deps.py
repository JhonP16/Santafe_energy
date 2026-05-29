"""Dependencias compartidas por las rutas de la API (FastAPI ``Depends``)."""
from typing import Annotated

from fastapi import Depends, Request

from app.services.catalog import Catalog, get_catalog
from app.services.xm_client import XMClient


def get_xm_client(request: Request) -> XMClient:
    """Obtiene el cliente de XM creado durante el ciclo de vida de la app."""
    return request.app.state.xm_client


# Alias de tipos para inyectar de forma concisa en las firmas de las rutas.
XMClientDep = Annotated[XMClient, Depends(get_xm_client)]
CatalogDep = Annotated[Catalog, Depends(get_catalog)]
