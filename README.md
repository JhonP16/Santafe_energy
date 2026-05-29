# Santafé Energy

Aplicación web (SPA) que consume la **API pública de XM** y presenta cuatro
paneles del sector energético colombiano: precios de bolsa, generación, demanda
comercial y volumen útil de embalses.

> Proyecto en construcción. Este README se irá completando a medida que se
> desarrollan los módulos.

## Arquitectura

```
Santafe_energy/
├── backend/          # API REST (FastAPI) que consume y procesa los datos de XM
│   └── app/
│       ├── core/     # Configuración y manejo de errores
│       ├── api/      # Rutas HTTP
│       ├── services/ # Cliente de la API XM y carga de catálogos (Excel)
│       ├── domain/   # Lógica de negocio (boxplot, top 10, alertas, etc.)
│       └── schemas/  # Modelos de respuesta (Pydantic)
├── frontend/         # SPA (React + Vite) — próximamente
├── recursos.xlsx     # Catálogo de recursos de generación (códigos SIC)
└── agentes.xlsx      # Catálogo de agentes (códigos SIC)
```

El **frontend nunca llama directamente a XM**: siempre pasa por el backend, que
encapsula el consumo de la API, la lógica de negocio y el mapeo de códigos.

## Tecnologías

- **Backend:** Python 3.11+, FastAPI, httpx, openpyxl, Pydantic.
- **Frontend:** React + Vite + Plotly.js *(en desarrollo)*.

## Puesta en marcha (backend)

```bash
cd backend
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
cp .env.example .env          # opcional: ajustar configuración

uvicorn app.main:app --reload
```

La API queda disponible en `http://localhost:8000`:

- Health check: `GET http://localhost:8000/api/health`
- Documentación interactiva (Swagger): `http://localhost:8000/docs`
