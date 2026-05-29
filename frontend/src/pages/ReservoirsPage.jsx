import { Loader, ErrorMessage, EmptyState, StatCard } from '../components/ui'
import { useAsync } from '../hooks/useAsync'
import { api } from '../api/client'
import { formatNumber } from '../utils/format'

export default function ReservoirsPage() {
  const { loading, error, data } = useAsync(() => api.getReservoirs(), [])

  const criticalCount = data?.reservoirs.filter((r) => r.is_critical).length ?? 0

  return (
    <>
      <header className="page-header">
        <h1>Volumen útil de embalses</h1>
        <p>
          Estado diario del volumen útil (%) de los embalses del sistema. Se
          resaltan en rojo los que están por debajo del {data?.threshold ?? 30}%.
        </p>
      </header>

      {loading && <Loader />}
      {error && <ErrorMessage message={error} />}
      {data && data.reservoirs.length === 0 && <EmptyState />}

      {data && data.reservoirs.length > 0 && (
        <>
          <div className="stats-grid">
            <StatCard label="Último dato registrado" value={data.date} />
            <StatCard label="Embalses monitoreados" value={data.reservoirs.length} />
            <StatCard
              label={`En alerta (< ${data.threshold}%)`}
              value={criticalCount}
              hint={criticalCount === 0 ? 'Sin embalses críticos' : 'Requieren atención'}
            />
          </div>

          <div className="card">
            <h3>Volumen útil al {data.date}</h3>
            <table className="table">
              <thead>
                <tr>
                  <th>Embalse</th>
                  <th>Volumen útil ({data.unit})</th>
                  <th>Estado</th>
                </tr>
              </thead>
              <tbody>
                {data.reservoirs.map((r) => (
                  <tr key={r.name} className={r.is_critical ? 'row-alert' : ''}>
                    <td>{r.name}</td>
                    <td>{formatNumber(r.volume)}</td>
                    <td>
                      <span className={`badge ${r.is_critical ? 'danger' : 'ok'}`}>
                        {r.is_critical ? 'Crítico' : 'Normal'}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}
    </>
  )
}
