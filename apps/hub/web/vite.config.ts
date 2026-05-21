import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'
import { VitePWA } from 'vite-plugin-pwa'

export default defineConfig({
  plugins: [
    react(),
    tailwindcss(),
    VitePWA({
      registerType: 'autoUpdate',
      injectRegister: null,
      includeAssets: ['logo.svg'],
      srcDir: 'src',
      filename: 'sw.ts',
      manifest: {
        id: 'hearth',
        name: 'Hearth',
        short_name: 'Hearth',
        description: 'Hearth Mantle shell',
        start_url: '/dashboard',
        scope: '/',
        display: 'standalone',
        background_color: '#0f1115',
        theme_color: '#0f1115',
        icons: [
          { src: '/logo.svg', sizes: '180x180', type: 'image/svg+xml', purpose: 'any' },
          { src: '/logo.svg', sizes: '192x192', type: 'image/svg+xml', purpose: 'any maskable' },
          { src: '/logo.svg', sizes: '512x512', type: 'image/svg+xml', purpose: 'any maskable' },
        ],
      },
      workbox: {
        globPatterns: ['**/*.{js,css,html,svg,png,webp,ico}'],
        // Only hub shell routes use the SPA fallback. Plugin iframes load /<slug>/… from
        // the network (Caddy → plugin container); a broad fallback served Mantle index.html
        // inside the iframe and showed PluginEmbedSurface instead of the plugin UI.
        navigateFallback: '/index.html',
        navigateFallbackAllowlist: [/^\/$/, /^\/dashboard(?:\/|$)/, /^\/settings(?:\/|$)/],
        navigateFallbackDenylist: [/^\/api\//],
      },
      devOptions: {
        enabled: true,
      },
    }),
  ],
  test: {
    environment: 'jsdom',
    setupFiles: ['./src/test/setup.ts'],
    globals: true,
  },
})
