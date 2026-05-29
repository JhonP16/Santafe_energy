import { useEffect, useState } from 'react'
import Plot from '../components/Plot'
import SearchSelect from '../components/SearchSelect'
import { Loader, ErrorMessage, EmptyState, StatCard } from '../components/ui'
import { useAsync } from '../hooks/useAsync'
import { api } from '../api/client'
import { formatNumber, daysAgo, yesterday } from '../utils/format'

export default function DemandPage() {
  const [agent, setAgent] = useState('')
  const [start, setStart] = useState(daysAgo(30))
  const [end, setEnd] = useState(yesterday())

  // Catálogo de comercializadores para el selector.
  const agents = useAsync(() => api.getComercializadores(), [])

  // Selecciona el primer comercializador por defecto al cargar la lista.
  useEffect(() => {
    if (!agent && agents.data?.length) {
      setAgent(agents.data[0].code)
    }
  }, [agents.data, agent])

  // Curva de demanda del agente seleccionado.
  const demand = useAsync(
    () => (agent ? api.getDemand(agent, start, end) : Promise.resolve(null)),
    [agent, start, end],
  )

  const options = (agents.data ?? []).map((a) => ({ value: a.code, label: a.name }))

  return (
    <>
      <header className="page-header">
        <h1>Panel de demanda</h1>
        <p>
          Curva de demanda comercial horaria (DemaCome) de un agente
          comercializador durante el periodo seleccionado.
        </p>
      </header>

      <div className="toolbar">
        <div className="field">
          <label htmlFor="agent">Comercializador</label>
          {agents.loading && <input disabled placeholder="Cargando agentes…" />}
          {agents.error && <input disabled placeholder="Error al cargar agentes" />}
          {agents.data && (
            <SearchSelect
              options={options}
              value={agent}
              onChange={setAgent}
              placeholder="Buscar o seleccionar comercializador…"
            />
          )}
        </div>
        <div className="field">
          <label htmlFor="start">Desde</label>
          <input id="start" type="date" value={start} max={end} onChange={(e) => setStart(e.target.value)} />
        </div>
        <div className="field">
          <label htmlFor="end">Hasta</label>
          <input id="end" type="date" value={end} max={yesterday()} onChange={(e) => setEnd(e.target.value)} />
        </div>
      </div>

      {demand.loading && <Loader />}
      {demand.error && <ErrorMessage message={demand.error} />}
      {!demand.loading && !demand.error && !demand.data && (
        <EmptyState message="Selecciona un comercializador para ver su demanda." />
      )}

      {demand.data && (
        <>
          <div className="stats-grid">
            <StatCard label="Agente" value={demand.data.agent_name} />
            <StatCard
              label="Demanda horaria promedio"
              value={`${formatNumber(demand.data.average)} ${demand.data.unit}`}
            />
          </div>

          <div className="card">
            <h3>Curva de demanda horaria · {demand.data.start} a {demand.data.end}</h3>
            <DemandLineChart points={demand.data.points} unit={demand.data.unit} />
          </div>
        </>
      )}
    </>
  )
}

function DemandLineChart({ points, unit }) {
  return (
    <Plot
      data={[
        {
          type: 'scatter',
          mode: 'lines',
          x: points.map((p) => p.timestamp),
          y: points.map((p) => p.value),
          line: { color: '#16a34a', width: 1.5 },
          fill: 'tozeroy',
          fillcolor: 'rgba(34, 197, 94, 0.12)',
          hovertemplate: `%{x|%d %b %H:%M}<br>%{y:.0f} ${unit}<extra></extra>`,
          connectgaps: false,
        },
      ]}
      layout={{
        autosize: true,
        height: 460,
        margin: { t: 20, r: 20, b: 50, l: 70 },
        xaxis: { type: 'date', gridcolor: '#eef2ef' },
        yaxis: { title: unit, gridcolor: '#eef2ef', zeroline: false },
        paper_bgcolor: 'transparent',
        plot_bgcolor: 'transparent',
      }}
      config={{ displayModeBar: false, responsive: true }}
      style={{ width: '100%' }}
      useResizeHandler
    />
  )
}
