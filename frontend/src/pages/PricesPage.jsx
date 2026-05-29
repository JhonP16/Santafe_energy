import { useState } from 'react'
import Plot from '../components/Plot'
import { Loader, ErrorMessage, StatCard } from '../components/ui'
import { useAsync } from '../hooks/useAsync'
import { api } from '../api/client'
import { formatNumber, yesterday } from '../utils/format'

export default function PricesPage() {
  const [day, setDay] = useState(yesterday())
  const { loading, error, data } = useAsync(() => api.getPrices(day), [day])

  return (
    <>
      <header className="page-header">
        <h1>Panel de precios</h1>
        <p>
          Distribución horaria del Precio de Bolsa Nacional (PrecBolsNaci) y
          promedio diario del sistema.
        </p>
      </header>

      <div className="toolbar">
        <div className="field">
          <label htmlFor="day">Día</label>
          <input
            id="day"
            type="date"
            value={day}
            max={yesterday()}
            onChange={(e) => setDay(e.target.value)}
          />
        </div>
      </div>

      {loading && <Loader />}
      {error && <ErrorMessage message={error} />}

      {data && (
        <>
          <div className="stats-grid">
            <StatCard
              label="Precio de bolsa promedio diario"
              value={`${formatNumber(data.average)} ${data.unit}`}
            />
            <StatCard
              label="Hora pico (máximo)"
              value={`${formatNumber(data.peak.value)}`}
              hint={`Hora ${data.peak.hour} · ${data.unit}`}
            />
            <StatCard
              label="Hora valle (mínimo)"
              value={`${formatNumber(data.lowest.value)}`}
              hint={`Hora ${data.lowest.hour} · ${data.unit}`}
            />
          </div>

          <div className="card">
            <h3>Box plot · 24 horas del {data.date}</h3>
            <PriceBoxPlot values={data.values} unit={data.unit} />
          </div>
        </>
      )}
    </>
  )
}

function PriceBoxPlot({ values, unit }) {
  const prices = values.map((v) => v.value)
  const hours = values.map((v) => `Hora ${v.hour}`)

  return (
    <Plot
      data={[
        {
          type: 'box',
          y: prices,
          name: 'Precio',
          boxmean: true,
          boxpoints: 'all',
          jitter: 0.4,
          pointpos: 0,
          marker: { color: '#16a34a', size: 6 },
          line: { color: '#15803d' },
          fillcolor: 'rgba(34, 197, 94, 0.15)',
          text: hours,
          hovertemplate: `%{text}<br>%{y:.2f} ${unit}<extra></extra>`,
        },
      ]}
      layout={{
        autosize: true,
        height: 460,
        margin: { t: 20, r: 20, b: 40, l: 60 },
        yaxis: { title: unit, zeroline: false, gridcolor: '#eef2ef' },
        xaxis: { showticklabels: false },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
        showlegend: false,
      }}
      config={{ displayModeBar: false, responsive: true }}
      style={{ width: '100%' }}
      useResizeHandler
    />
  )
}
