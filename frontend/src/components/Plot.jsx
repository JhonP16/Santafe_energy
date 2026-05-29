import { lazy, Suspense } from 'react'

// Plotly es pesado (~1.5 MB gzip). Se carga como chunk independiente y solo
// cuando se monta una gráfica, manteniendo liviano el bundle inicial.
const LazyPlot = lazy(() =>
  Promise.all([
    import('plotly.js-dist-min'),
    import('react-plotly.js/factory'),
  ]).then(([plotly, factory]) => ({
    default: factory.default(plotly.default),
  })),
)

// Envoltura con su propio límite de Suspense: mientras Plotly se descarga,
// solo el área de la gráfica muestra el spinner (los filtros permanecen).
export default function Plot(props) {
  return (
    <Suspense
      fallback={
        <div className="state">
          <div className="spinner" />
        </div>
      }
    >
      <LazyPlot {...props} />
    </Suspense>
  )
}
