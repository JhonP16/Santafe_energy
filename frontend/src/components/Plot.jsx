// Wrapper de Plotly usando la distribución reducida (plotly.js-dist-min)
// para mantener el bundle más liviano que el paquete completo.
import Plotly from 'plotly.js-dist-min'
import createPlotlyComponent from 'react-plotly.js/factory'

const Plot = createPlotlyComponent(Plotly)

export default Plot
