# Reto técnico: Desarrollo de aplicación web - Sector energético

## Tarea
Se solicita la construcción de una aplicación de página única (Single Page Application - SPA) que consuma la API de XM y conste de cuatro secciones principales dispuestas en un menú lateral.

---

## Módulos de la Aplicación

| Sección | Métrica (`MetricId`) | Periodicidad / Endpoint | Entidad | Requerimiento Técnico |
| :--- | :--- | :--- | :--- | :--- |
| **1. Panel de precios** | `PrecBolsNaci` | Horaria<br>([Endpoint Hourly](https://servapibi.xm.com.co/hourly)) | Sistema | Graficar un *box plot* para las 24 horas del día seleccionado para identificar picos de energía y calcular automáticamente el Precio de Bolsa Promedio diario. |
| **2. Panel de generación** | `Gene` | Horaria<br>(Endpoint `hourly`) | Recurso | Agrupar la generación total por planta (dentro del rango de fechas provisto), ordenarla de mayor a menor y desplegar un *Top 10* de Plantas Despachadas Centralmente (DC) en un gráfico de barras. |
| **3. Panel de demanda** | `DemaCome` | Horaria<br>(Endpoint `hourly`) | Agente o MercadoComercializacion | Implementar un sistema de filtrado avanzado donde el usuario pueda buscar o seleccionar un agente comercializador específico (ej. EPM, EMGESA) y visualizar su curva de demanda horaria en un periodo de 1 mes. |
| **4. Panel del volumen vtil** | `PorcVoluUtilDiar` | Diaria<br>([Endpoint Daily](https://servapibi.xm.com.co/daily)) | Embalse | Presentar una tabla con el estado diario del volumen útil (%) de embalses críticos (ej. Guatapé, Topocoro o El Peñol), incluyendo alertas visuales (ej. resaltar en color rojo si el nivel es inferior al 30%).Debe realziarse para  el ultimo dato registrado en el llamdo de la API y debe mostrarse ese dia en el encabzado de la tabla|

> **Nota de desarrollo para filtros:** Para la correcta segmentación de los paneles de producción y consumo, el postulante deberá apoyarse en los listados de recursos y agentes comercializadores provistos en la documentación de la API, ademas de que se daran con extension de EXCEL.

---

## Requisitos Técnicos

* **Tecnología:** El *stack* de desarrollo es de libre elección (se admite el uso de React, Angular, JavaScript, Python entre otros).
* **Gestión de Errores:** La aplicación debe ser robusta y controlar de forma adecuada las excepciones; ante fallos de la API o ausencia de datos, se debe mostrar un mensaje claro y amigable al usuario.
* **Interfaz de Usuario:** El diseño debe ser limpio, intuitivo y contar con un diseño responsivo que garantice su correcta visualización en dispositivos móviles.

---

## Entregables

* **Repositorio código:** El código fuente debe ser alojado en un repositorio público de GitHub.
* **Historial de commits:** Se evaluará el progreso evolutivo del desarrollo. Se deben realizar commits significativos y estructurados a lo largo del proceso (ej. `feat: setup del proyecto`, `feat: consumo de api exitoso`, `fix: diseño responsivo`), evitando cargar todo el proyecto en un único registro.
* **Documentación (README.md):** El repositorio debe incluir un archivo informativo rigguoso que contenga:
    * Nombre del proyecto junto con una breve descripción técnica.
    * Guía de instalación paso a paso detallando la clonación del repositorio, instalación de dependencias y comandos para la ejecución en el entorno local.
    * Listado explícito de las tecnologías y librerías utilizadas.
* **Despliegue (puntos extras):** La publicación de la aplicación en plataformas de hosting gratuito (ej. Vercel, Netlify, GitHub Pages) con su respectivo enlace en el README sumará puntos adicionales a la calificación global.

---
> **Documentación de Referencia:** [API XM en GitHub](https://github.com/EquipoAnaliticaXM/API_XM)
