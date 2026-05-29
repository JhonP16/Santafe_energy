import { useEffect, useRef, useState } from 'react'

// Combobox buscable: el usuario puede escribir para filtrar o desplegar la lista
// y seleccionar. Las opciones tienen forma { value, label }.
export default function SearchSelect({ options, value, onChange, placeholder }) {
  const [query, setQuery] = useState('')
  const [open, setOpen] = useState(false)
  const containerRef = useRef(null)

  const selected = options.find((o) => o.value === value)

  // Cierra el desplegable al hacer clic fuera del componente.
  useEffect(() => {
    function onClickOutside(event) {
      if (containerRef.current && !containerRef.current.contains(event.target)) {
        setOpen(false)
      }
    }
    document.addEventListener('mousedown', onClickOutside)
    return () => document.removeEventListener('mousedown', onClickOutside)
  }, [])

  const filtered = options
    .filter((o) => o.label.toLowerCase().includes(query.toLowerCase()))
    .slice(0, 50)

  function handleSelect(option) {
    onChange(option.value)
    setOpen(false)
    setQuery('')
  }

  return (
    <div className="search-select" ref={containerRef}>
      <input
        type="text"
        placeholder={placeholder}
        value={open ? query : selected?.label ?? ''}
        onFocus={() => {
          setOpen(true)
          setQuery('')
        }}
        onChange={(e) => {
          setQuery(e.target.value)
          setOpen(true)
        }}
      />

      {open && (
        <ul className="search-select-list">
          {filtered.length === 0 && (
            <li className="search-select-empty">Sin coincidencias</li>
          )}
          {filtered.map((option) => (
            <li
              key={option.value}
              className={option.value === value ? 'active' : ''}
              onMouseDown={() => handleSelect(option)}
            >
              {option.label}
            </li>
          ))}
        </ul>
      )}
    </div>
  )
}
