// Cliente HTTP del frontend hacia el backend.
// En desarrollo, VITE_API_URL queda vacío y se usa el proxy de Vite (/api).
const BASE_URL = import.meta.env.VITE_API_URL ?? ''

async function request(path) {
  let response
  try {
    response = await fetch(`${BASE_URL}/api${path}`)
  } catch {
    throw new Error('No se pudo conectar con el servidor. Verifica tu conexión.')
  }

  if (!response.ok) {
    let detail = 'Ocurrió un error inesperado al consultar los datos.'
    try {
      const data = await response.json()
      if (data?.detail) detail = data.detail
    } catch {
      // respuesta sin cuerpo JSON: se conserva el mensaje por defecto
    }
    throw new Error(detail)
  }

  return response.json()
}

export const api = {
  getPrices: (day) => request(`/prices?day=${day}`),
  getGeneration: (start, end, limit = 10) =>
    request(`/generation?start=${start}&end=${end}&limit=${limit}`),
  getDemand: (agent, start, end) =>
    request(`/demand?agent=${encodeURIComponent(agent)}&start=${start}&end=${end}`),
  getComercializadores: () => request('/catalog/comercializadores'),
}
