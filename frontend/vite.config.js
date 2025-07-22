import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: '/eth-market-forecasting/',
  plugins: [react()],
});
