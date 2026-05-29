// Utilidades de formato numérico y de fechas (configuración regional Colombia).

const numberFormatter = new Intl.NumberFormat('es-CO', {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
})

export function formatNumber(value) {
  if (value === null || value === undefined || Number.isNaN(value)) return '—'
  return numberFormatter.format(value)
}

// Devuelve la fecha (Date) como cadena 'YYYY-MM-DD' en horario local.
export function toISODate(date) {
  const offset = date.getTimezoneOffset() * 60000
  return new Date(date.getTime() - offset).toISOString().slice(0, 10)
}

export function yesterday() {
  const d = new Date()
  d.setDate(d.getDate() - 1)
  return toISODate(d)
}
