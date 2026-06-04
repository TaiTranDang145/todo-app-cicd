import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Cấu hình cổng chạy frontend là 3000
export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    host: true,
    strictPort: true
  }
})
