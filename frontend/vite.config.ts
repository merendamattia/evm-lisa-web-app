import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  resolve: {
    alias: {
      '@': '/src', // Alias per il percorso della cartella src
    }
  },
  plugins: [vue()],
})
