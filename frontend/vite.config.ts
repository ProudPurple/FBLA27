import tailwindcss from '@tailwindcss/vite'
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  // Relative asset paths so the built index.html works when pywebview
  // loads it straight off disk (file://) as well as from a dev server.
  base: './',
  plugins: [react(), tailwindcss()],
  build: {
    outDir: '../backend/frontend_dist',
    emptyOutDir: true,
  },
})
