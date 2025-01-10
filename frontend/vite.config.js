import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  server: {
    host: '0.0.0.0', // Bind to all interfaces
    port: 5173,      // Default port
    logLevel: 'error',
    strictPort: true // Ensure port 5173 is used
  },
  plugins: [react()],
});