# Santafé Energy 

Aplicación web de página única (**SPA**) que consume la **API pública de XM**
(operador del mercado eléctrico colombiano) y presenta cuatro paneles
analíticos del sector energético:

1. **Panel de precios** — Box plot de las 24 horas del Precio de Bolsa Nacional
   (`PrecBolsNaci`) y cálculo automático del precio de bolsa promedio diario.
2. **Panel de generación** — Top 10 de plantas de Despacho Central (DC) por
   generación total (`Gene`) en un rango de fechas, en gráfico de barras.
3. **Panel de demanda** — Curva de demanda comercial horaria (`DemaCome`) de un
   agente comercializador seleccionable, durante un periodo de hasta un mes.
4. **Panel de volumen útil** — Tabla del volumen útil diario (%) de los embalses
   (`PorcVoluUtilDiar`) en el último día registrado, con alertas en rojo para
   niveles inferiores al 30%.

## Descripción técnica

El proyecto está dividido en dos componentes desacoplados:

- **Backend (FastAPI):** actúa como capa intermedia entre el frontend y la API
  de XM. Encapsula el consumo de la API, **normaliza** las respuestas (de
  formato anidado a estructuras simples), aplica la **lógica de negocio** de
  cada panel (estadísticas del box plot, agregación y ranking de generación,
  serie temporal de demanda, detección del último día y alertas de embalses) y
  **enriquece** los datos cruzando los códigos SIC con los catálogos en Excel
  (`recursos.xlsx`, `agentes.xlsx`).
- **Frontend (React + Vite):** SPA con menú lateral y cuatro vistas. **Nunca
  llama directamente a XM**; siempre consume el backend. Las gráficas se
  renderizan con Plotly (cargado bajo demanda mediante *code-splitting*).

```
Frontend (React)  ──►  Backend (FastAPI)  ──►  API XM (servapibi.xm.com.co)
                                          └──►  Catálogos Excel (códigos SIC)
```

## Estructura del repositorio

```
Santafe_energy/
├── backend/
│   ├── app/
│   │   ├── main.py            # App FastAPI (factory + lifespan + CORS)
│   │   ├── core/              # Configuración y manejo de errores
│   │   ├── api/
│   │   │   ├── deps.py        # Inyección de dependencias
│   │   │   └── routes/        # Endpoints por módulo
│   │   ├── services/          # Cliente HTTP de XM y carga de catálogos
│   │   ├── domain/            # Lógica de negocio (pura, testeable)
│   │   └── schemas/           # Modelos de respuesta (Pydantic)
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── api/               # Cliente HTTP hacia el backend
│       ├── components/        # Sidebar, Plot, SearchSelect, UI
│       ├── hooks/             # useAsync
│       ├── pages/             # Una página por panel
│       └── utils/             # Formato numérico y de fechas
├── recursos.xlsx              # Catálogo de recursos de generación
├── agentes.xlsx               # Catálogo de agentes del mercado
├── render.yaml                # Despliegue del backend (Render)
└── frontend/vercel.json       # Despliegue del frontend (Vercel)
```

## Tecnologías y librerías

**Backend**
- Python 3.11+ · [FastAPI](https://fastapi.tiangolo.com/) · [Uvicorn](https://www.uvicorn.org/)
- [httpx](https://www.python-httpx.org/) — cliente HTTP asíncrono hacia la API de XM
- [openpyxl](https://openpyxl.readthedocs.io/) — lectura de los catálogos Excel
- [Pydantic](https://docs.pydantic.dev/) / pydantic-settings — validación y configuración

**Frontend**
- [React 18](https://react.dev/) · [Vite](https://vitejs.dev/) · [React Router](https://reactrouter.com/)
- [Plotly.js](https://plotly.com/javascript/) (`react-plotly.js`) — box plot, barras y series temporales

## Requisitos previos

- [Python 3.11 o superior](https://www.python.org/downloads/)
- [Node.js 18 o superior](https://nodejs.org/) (incluye npm)

## Instalación y ejecución local

### 1. Clonar el repositorio

```bash
git clone https://github.com/JhonP16/Santafe_energy.git
cd Santafe_energy
```

### 2. Backend (FastAPI)

```bash
cd backend
python -m venv .venv

# Activar el entorno virtual
.venv\Scripts\activate        # Windows
source .venv/bin/activate      # Linux / macOS

pip install -r requirements.txt
cp .env.example .env           # opcional: ajustar configuración

uvicorn app.main:app --reload
```

El backend queda disponible en `http://localhost:8000`:
- Documentación interactiva (Swagger): `http://localhost:8000/docs`
- Health check: `http://localhost:8000/api/health`

### 3. Frontend (React + Vite)

En **otra terminal**:

```bash
cd frontend
npm install
npm run dev
```

La aplicación abre en `http://localhost:5173`. En desarrollo, las peticiones a
`/api` se redirigen automáticamente al backend mediante el proxy de Vite.

## Endpoints del backend

| Método | Endpoint | Descripción |
| :--- | :--- | :--- |
| `GET` | `/api/health` | Estado del servicio |
| `GET` | `/api/prices?day=YYYY-MM-DD` | Precio de bolsa horario y promedio diario |
| `GET` | `/api/generation?start&end&limit` | Top de plantas DC por generación |
| `GET` | `/api/demand?agent&start&end` | Curva de demanda horaria de un agente |
| `GET` | `/api/reservoirs` | Volumen útil de embalses (último día) |
| `GET` | `/api/catalog/comercializadores` | Listado de agentes comercializadores |

## Manejo de errores

El backend centraliza el manejo de excepciones: ante fallos de la API de XM
(timeout, error HTTP, respuesta inválida) o ausencia de datos, responde con un
JSON consistente (`{"detail": "..."}`) y un mensaje claro que el frontend
muestra al usuario. También valida el rango máximo de 30 días de la API.

## Despliegue

El proyecto incluye configuración lista para hosting gratuito:

- **Backend → [Render](https://render.com/):** el archivo `render.yaml` define el
  Web Service. Tras crearlo, configurar la variable de entorno `CORS_ORIGINS`
  con la URL del frontend desplegado.
- **Frontend → [Vercel](https://vercel.com/):** `frontend/vercel.json` configura
  el build de Vite y el enrutado SPA. Definir la variable `VITE_API_URL` con la
  URL del backend desplegado. (También incluye `public/_redirects` para Netlify.)

> 🔗 **Demo en vivo:** _pendiente de despliegue — se actualizará el enlace aquí._


## Este readme fue realizado con ayuda de Claude.