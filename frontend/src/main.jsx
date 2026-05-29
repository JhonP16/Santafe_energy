import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'
import App from './App'
import PricesPage from './pages/PricesPage'
import ComingSoonPage from './pages/ComingSoonPage'
import './index.css'

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Navigate to="/precios" replace /> },
      { path: 'precios', element: <PricesPage /> },
      { path: 'generacion', element: <ComingSoonPage title="Panel de generación" /> },
      { path: 'demanda', element: <ComingSoonPage title="Panel de demanda" /> },
      { path: 'volumen-util', element: <ComingSoonPage title="Volumen útil" /> },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
