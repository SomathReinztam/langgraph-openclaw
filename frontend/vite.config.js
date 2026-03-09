import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/users': 'http://localhost:8000',
      '/chats': 'http://localhost:8000',
      '/runeduchat': 'http://localhost:8000',
    },
  },
})
