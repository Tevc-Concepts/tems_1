/**
 * TEMS Service Worker
 * Provides offline functionality and caching for the PWA
 */

const CACHE_NAME = 'tems-cache-v1';
const urlsToCache = [
    '/',
    '/assets/tems/css/tems_theme.css',
    '/assets/tems/js/landing.js',
    '/assets/tems/manifest.json',
    '/driver',
    '/operations',
    '/fleet',
    '/safety'
];

// Install event - cache essential resources
self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then((cache) => {
                console.log('TEMS: Opened cache');
                return cache.addAll(urlsToCache);
            })
            .then(() => {
                return self.skipWaiting();
            })
    );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== CACHE_NAME) {
                        console.log('TEMS: Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            return self.clients.claim();
        })
    );
});

// Fetch event - serve from cache, fallback to network
self.addEventListener('fetch', (event) => {
    // Skip cross-origin requests
    if (!event.request.url.startsWith(self.location.origin)) {
        return;
    }

    // Skip API requests for live data (always fetch fresh)
    if (event.request.url.includes('/api/method/')) {
        event.respondWith(
            fetch(event.request).catch(() => {
                return new Response(
                    JSON.stringify({ message: 'Offline - cached data not available' }),
                    { headers: { 'Content-Type': 'application/json' } }
                );
            })
        );
        return;
    }

    // Network first, fall back to cache
    event.respondWith(
        fetch(event.request)
            .then((response) => {
                // Clone the response
                const responseToCache = response.clone();

                caches.open(CACHE_NAME).then((cache) => {
                    cache.put(event.request, responseToCache);
                });

                return response;
            })
            .catch(() => {
                // Network request failed, try cache
                return caches.match(event.request).then((response) => {
                    if (response) {
                        return response;
                    }

                    // If not in cache, return offline page
                    return new Response(
                        '<html><body><h1>TEMS - Offline</h1><p>You are currently offline. Please check your connection.</p></body></html>',
                        { headers: { 'Content-Type': 'text/html' } }
                    );
                });
            })
    );
});

// Background sync
self.addEventListener('sync', (event) => {
    if (event.tag === 'sync-metrics') {
        event.waitUntil(syncMetrics());
    }
});

async function syncMetrics() {
    try {
        const response = await fetch('/api/method/tems.tems.www.index.get_live_metrics');
        const data = await response.json();
        
        // Broadcast to all clients
        const clients = await self.clients.matchAll();
        clients.forEach(client => {
            client.postMessage({
                type: 'METRICS_UPDATED',
                data: data.message
            });
        });
    } catch (error) {
        console.error('TEMS: Failed to sync metrics:', error);
    }
}

// Push notifications
self.addEventListener('push', (event) => {
    const options = {
        body: event.data ? event.data.text() : 'New update from TEMS',
        icon: '/assets/tems/images/icon-192x192.png',
        badge: '/assets/tems/images/badge-72x72.png',
        vibrate: [200, 100, 200],
        data: {
            dateOfArrival: Date.now(),
            primaryKey: 1
        },
        actions: [
            {
                action: 'explore',
                title: 'View Details',
                icon: '/assets/tems/images/checkmark.png'
            },
            {
                action: 'close',
                title: 'Dismiss',
                icon: '/assets/tems/images/close.png'
            }
        ]
    };

    event.waitUntil(
        self.registration.showNotification('TEMS Notification', options)
    );
});

// Notification click
self.addEventListener('notificationclick', (event) => {
    event.notification.close();

    if (event.action === 'explore') {
        event.waitUntil(
            clients.openWindow('/')
        );
    }
});

// Message handler
self.addEventListener('message', (event) => {
    if (event.data && event.data.type === 'SKIP_WAITING') {
        self.skipWaiting();
    }
});

console.log('TEMS Service Worker loaded');
