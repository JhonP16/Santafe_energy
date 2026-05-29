import { Suspense, useState } from 'react'
import { Outlet } from 'react-router-dom'
import Sidebar from './components/Sidebar'
import { Loader } from './components/ui'

export default function App() {
  const [menuOpen, setMenuOpen] = useState(false)

  return (
    <div className="app">
      <button
        className="menu-toggle"
        onClick={() => setMenuOpen((v) => !v)}
        aria-label="Abrir menú"
      >
        ☰
      </button>

      <Sidebar open={menuOpen} onNavigate={() => setMenuOpen(false)} />

      {menuOpen && <div className="backdrop" onClick={() => setMenuOpen(false)} />}

      <main className="content">
        <Suspense fallback={<Loader />}>
          <Outlet />
        </Suspense>
      </main>
    </div>
  )
}
