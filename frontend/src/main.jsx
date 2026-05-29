import React, { lazy } from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'
import App from './App'
import './index.css'

// Carga diferida de las páginas: cada panel se descarga solo al visitarlo.
const PricesPage = lazy(() => import('./pages/PricesPage'))
const GenerationPage = lazy(() => import('./pages/GenerationPage'))
const DemandPage = lazy(() => import('./pages/DemandPage'))
const ReservoirsPage = lazy(() => import('./pages/ReservoirsPage'))

const router = createBrowserRouter([
  {
    path: '/',
    element: <App />,
    children: [
      { index: true, element: <Navigate to="/precios" replace /> },
      { path: 'precios', element: <PricesPage /> },
      { path: 'generacion', element: <GenerationPage /> },
      { path: 'demanda', element: <DemandPage /> },
      { path: 'volumen-util', element: <ReservoirsPage /> },
    ],
  },
])

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router} />
  </React.StrictMode>,
)
