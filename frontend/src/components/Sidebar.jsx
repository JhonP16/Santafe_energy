import { NavLink } from 'react-router-dom'

const LINKS = [
  { to: '/precios', label: 'Panel de precios', icon: '💲' },
  { to: '/generacion', label: 'Panel de generación', icon: '⚡' },
  { to: '/demanda', label: 'Panel de demanda', icon: '📈' },
  { to: '/volumen-util', label: 'Volumen útil', icon: '💧' },
]

export default function Sidebar({ open, onNavigate }) {
  return (
    <aside className={`sidebar ${open ? 'open' : ''}`}>
      <div className="brand">
        <div className="logo">SE</div>
        <div>
          <div className="brand-name">Santafé Energy</div>
          <div className="brand-sub">Datos del mercado XM</div>
        </div>
      </div>

      <nav className="nav">
        {LINKS.map((link) => (
          <NavLink
            key={link.to}
            to={link.to}
            className="nav-link"
            onClick={onNavigate}
          >
            <span className="nav-icon">{link.icon}</span>
            {link.label}
          </NavLink>
        ))}
      </nav>
    </aside>
  )
}
