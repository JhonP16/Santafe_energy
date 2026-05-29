import { useState } from 'react'
import Plot from '../components/Plot'
import { Loader, ErrorMessage, EmptyState } from '../components/ui'
import { useAsync } from '../hooks/useAsync'
import { api } from '../api/client'
import { daysAgo, yesterday } from '../utils/format'

export default function GenerationPage() {
  const [start, setStart] = useState(daysAgo(7))
  const [end, setEnd] = useState(yesterday())

  const { loading, error, data } = useAsync(
    () => api.getGeneration(start, end),
    [start, end],
  )

  return (
    <>
      <header className="page-header">
        <h1>Panel de generación</h1>
        <p>
          Top 10 de plantas de Despacho Central (DC) por generación total
          acumulada (Gene) en el rango seleccionado.
        </p>
      </header>

      <div className="toolbar">
        <div className="field">
          <label htmlFor="start">Desde</label>
          <input
            id="start"
            type="date"
            value={start}
            max={end}
            onChange={(e) => setStart(e.target.value)}
          />
        </div>
        <div className="field">
          <label htmlFor="end">Hasta</label>
          <input
            id="end"
            type="date"
            value={end}
            max={yesterday()}
            onChange={(e) => setEnd(e.target.value)}
          />
        </div>
      </div>

      {loading && <Loader />}
      {error && <ErrorMessage message={error} />}
      {data && data.plants.length === 0 && <EmptyState />}

      {data && data.plants.length > 0 && (
        <div className="card">
          <h3>Top {data.plants.length} plantas DC · {data.unit}</h3>
          <GenerationBarChart plants={data.plants} unit={data.unit} />
        </div>
      )}
    </>
  )
}

function GenerationBarChart({ plants, unit }) {
  // Plotly dibuja las barras horizontales de abajo hacia arriba según el orden
  // del arreglo; se invierte para que la planta con mayor generación quede arriba.
  const ordered = [...plants].reverse()

  return (
    <Plot
      data={[
        {
          type: 'bar',
          orientation: 'h',
          x: ordered.map((p) => p.total),
          y: ordered.map((p) => p.name),
          marker: { color: '#22c55e' },
          hovertemplate: `%{y}<br>%{x:.2f} ${unit}<extra></extra>`,
        },
      ]}
      layout={{
        autosize: true,
        height: 460,
        margin: { t: 20, r: 20, b: 40, l: 150 },
        xaxis: { title: `Generación (${unit})`, gridcolor: '#eef2ef', zeroline: false },
        yaxis: { automargin: true },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
      }}
      config={{ displayModeBar: false, responsive: true }}
      style={{ width: '100%' }}
      useResizeHandler
    />
  )
}
