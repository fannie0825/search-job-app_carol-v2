import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    open: true
  },
  base: process.env.VITE_BASE_PATH || '/',
  build: {
    outDir: 'dist',
    sourcemap: false,
  },
  // Expose REACT_APP_ environment variables for compatibility
  define: {
    'process.env.REACT_APP_API_URL': JSON.stringify(process.env.REACT_APP_API_URL || process.env.VITE_API_URL || 'http://localhost:8000/api'),
    'process.env.REACT_APP_USE_MOCK_API': JSON.stringify(process.env.REACT_APP_USE_MOCK_API || process.env.VITE_USE_MOCK_API || (!process.env.REACT_APP_API_URL && !process.env.VITE_API_URL ? 'true' : 'false')),
    'process.env.REACT_APP_AZURE_OPENAI_API_KEY': JSON.stringify(process.env.REACT_APP_AZURE_OPENAI_API_KEY || process.env.VITE_AZURE_OPENAI_API_KEY || ''),
    'process.env.REACT_APP_AZURE_OPENAI_ENDPOINT': JSON.stringify(process.env.REACT_APP_AZURE_OPENAI_ENDPOINT || process.env.VITE_AZURE_OPENAI_ENDPOINT || ''),
    'process.env.REACT_APP_RAPIDAPI_KEY': JSON.stringify(process.env.REACT_APP_RAPIDAPI_KEY || process.env.VITE_RAPIDAPI_KEY || ''),
    'process.env.REACT_APP_BACKEND_API_KEY': JSON.stringify(process.env.REACT_APP_BACKEND_API_KEY || process.env.VITE_BACKEND_API_KEY || ''),
  }
})
