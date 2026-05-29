// Componentes de presentación reutilizables (estados, tarjetas).

export function Loader({ message = 'Cargando datos…' }) {
  return (
    <div className="state">
      <div className="spinner" />
      <p>{message}</p>
    </div>
  )
}

export function ErrorMessage({ message }) {
  return (
    <div className="state error">
      <strong>No se pudieron cargar los datos</strong>
      <p>{message}</p>
    </div>
  )
}

export function EmptyState({ message = 'No hay datos para mostrar.' }) {
  return (
    <div className="state">
      <p>{message}</p>
    </div>
  )
}

export function StatCard({ label, value, hint }) {
  return (
    <div className="card stat-card">
      <div className="stat-label">{label}</div>
      <div className="stat-value">{value}</div>
      {hint && <div className="stat-hint">{hint}</div>}
    </div>
  )
}
