// Marcador de posición para los módulos aún no implementados.
export default function ComingSoonPage({ title }) {
  return (
    <>
      <header className="page-header">
        <h1>{title}</h1>
      </header>
      <div className="card">
        <div className="state">
          <p>Este módulo estará disponible próximamente.</p>
        </div>
      </div>
    </>
  )
}
