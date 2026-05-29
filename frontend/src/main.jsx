import React from 'react'
import ReactDOM from 'react-dom/client'
import { createBrowserRouter, Navigate, RouterProvider } from 'react-router-dom'
import App from './App'
import PricesPage from './pages/PricesPage'
import GenerationPage from './pages/GenerationPage'
import DemandPage from './pages/DemandPage'
import ReservoirsPage from './pages/ReservoirsPage'
import './index.css'

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
