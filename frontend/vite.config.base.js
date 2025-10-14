import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { VitePWA } from 'vite-plugin-pwa'
import path from 'path'

/**
 * Base Vite configuration for TEMS PWAs
 * Extend this in each PWA's vite.config.js
 */
export function createPWAConfig(pwaName, displayName, themeColor = '#36454f') {
    const rootDir = path.dirname(new URL(import.meta.url).pathname)

    return defineConfig({
        plugins: [
            vue(),
            VitePWA({
                registerType: 'autoUpdate',
                includeAssets: ['favicon.ico', 'logo.svg', 'robots.txt'],
                manifest: {
                    name: `TEMS ${displayName}`,
                    short_name: displayName,
                    description: `Transportation Enterprise Management - ${displayName} Portal`,
                    theme_color: themeColor,
                    background_color: '#e0e2db',
                    display: 'standalone',
                    orientation: 'portrait',
                    scope: `/${pwaName}/`,
                    start_url: `/${pwaName}/`,
                    icons: [
                        {
                            src: `/assets/tems/frontend/${pwaName}/dist/pwa-192x192.png`,
                            sizes: '192x192',
                            type: 'image/png'
                        },
                        {
                            src: `/assets/tems/frontend/${pwaName}/dist/pwa-512x512.png`,
                            sizes: '512x512',
                            type: 'image/png',
                            purpose: 'any maskable'
                        }
                    ]
                },
                workbox: {
                    globPatterns: ['**/*.{js,css,html,ico,png,svg,woff2}'],
                    runtimeCaching: [
                        {
                            urlPattern: /^https:\/\/.*\/api\/.*/i,
                            handler: 'NetworkFirst',
                            options: {
                                cacheName: 'api-cache',
                                expiration: {
                                    maxEntries: 100,
                                    maxAgeSeconds: 86400 // 24 hours
                                },
                                cacheableResponse: {
                                    statuses: [0, 200]
                                }
                            }
                        },
                        {
                            urlPattern: /^https:\/\/.*\.(png|jpg|jpeg|svg|gif)$/i,
                            handler: 'CacheFirst',
                            options: {
                                cacheName: 'image-cache',
                                expiration: {
                                    maxEntries: 50,
                                    maxAgeSeconds: 2592000 // 30 days
                                }
                            }
                        }
                    ]
                },
                devOptions: {
                    enabled: true
                }
            })
        ],
        resolve: {
            alias: {
                '@': path.resolve(rootDir, pwaName, 'src'),
                '@shared': path.resolve(rootDir, 'shared/src'),
            },
        },
        base: `/assets/tems/frontend/${pwaName}/dist/`,
        build: {
            outDir: `../../tems/public/frontend/${pwaName}/dist`,
            emptyOutDir: true,
            sourcemap: true,
            rollupOptions: {
                output: {
                    manualChunks: {
                        'vue-vendor': ['vue', 'vue-router', 'pinia'],
                        'utils': ['date-fns', 'localforage']
                    }
                }
            }
        },
        server: {
            port: parseInt(process.env.PORT) || 5173,
            proxy: {
                '/api': {
                    target: 'http://localhost:8000',
                    changeOrigin: true,
                },
                '/assets': {
                    target: 'http://localhost:8000',
                    changeOrigin: true,
                }
            }
        }
    })
}
