import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: parseInt(process.env.VITE_PORT) || 5000,
    strictPort: false,
    allowedHosts: true,
    proxy: {
      "/api": {
        target: "http://localhost:3000", // ✅ CHANGED FROM 8000 TO 3000
        changeOrigin: true,
        secure: false,
      },
    },
  },
});
