import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// En desarrollo, las peticiones a /api se redirigen al backend FastAPI.
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': 'http://localhost:8000',
    },
  },
})
