import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import svgr from "vite-plugin-svgr"

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), svgr()],
  server: {
    host: "0.0.0.0",
    watch: {
      usePolling: true,
      interval: 100
    },
    proxy: {
      "/api": {
        target: "http://backend:8000",
        changeOrigin: true
      }
    }
  }
})
