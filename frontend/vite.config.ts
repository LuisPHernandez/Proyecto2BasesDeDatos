import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import svgr from "vite-plugin-svgr"

// https://vite.dev/config/
export default defineConfig({
  base: '/proyecto2/',
  plugins: [react(), svgr()],
  server: {
    host: "0.0.0.0",
    watch: {
      usePolling: true,
      interval: 100
    },
    proxy: {
      "/api": {
        // target: "http://backend:8867",
        target: "http://34.51.81.158:8867",
        changeOrigin: true
      }
    }
  }
})
