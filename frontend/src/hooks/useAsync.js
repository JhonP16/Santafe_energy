import { useCallback, useEffect, useState } from 'react'

// Hook genérico para ejecutar una función asíncrona y exponer
// los estados de carga, error y datos. Reutilizado por todas las páginas.
export function useAsync(asyncFn, deps = []) {
  // eslint-disable-next-line react-hooks/exhaustive-deps
  const memoizedFn = useCallback(asyncFn, deps)
  const [state, setState] = useState({ loading: true, error: null, data: null })

  useEffect(() => {
    let active = true
    setState({ loading: true, error: null, data: null })

    memoizedFn()
      .then((data) => active && setState({ loading: false, error: null, data }))
      .catch((err) => active && setState({ loading: false, error: err.message, data: null }))

    return () => {
      active = false
    }
  }, [memoizedFn])

  return state
}
