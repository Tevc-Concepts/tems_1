import { ref, onMounted, onUnmounted } from 'vue'

/**
 * Push notifications composable
 * Handles push notification permissions and subscriptions
 * 
 * @returns {object} Notification state and methods
 * 
 * @example
 * ```javascript
 * import { useNotifications } from '@shared/composables/useNotifications'
 * 
 * const { 
 *   permission, 
 *   isSupported, 
 *   requestPermission,
 *   showNotification 
 * } = useNotifications()
 * 
 * // Request permission
 * await requestPermission()
 * 
 * // Show notification
 * showNotification('New Message', {
 *   body: 'You have a new message',
 *   icon: '/icon.png',
 *   badge: '/badge.png'
 * })
 * ```
 */
export function useNotifications() {
    const permission = ref(Notification?.permission || 'default')
    const isSupported = ref('Notification' in window)
    const serviceWorkerRegistration = ref(null)

    /**
     * Request notification permission
     * @returns {Promise<string>} Permission status
     */
    async function requestPermission() {
        if (!isSupported.value) {
            throw new Error('Notifications are not supported')
        }

        if (permission.value === 'granted') {
            return 'granted'
        }

        try {
            const result = await Notification.requestPermission()
            permission.value = result
            return result
        } catch (error) {
            console.error('Error requesting notification permission:', error)
            throw error
        }
    }

    /**
     * Show a notification
     * @param {string} title - Notification title
     * @param {object} options - Notification options
     * @returns {Notification}
     */
    function showNotification(title, options = {}) {
        if (!isSupported.value) {
            console.warn('Notifications are not supported')
            return null
        }

        if (permission.value !== 'granted') {
            console.warn('Notification permission not granted')
            return null
        }

        const defaultOptions = {
            icon: '/assets/tems/frontend/driver-pwa/dist/pwa-192x192.png',
            badge: '/assets/tems/frontend/driver-pwa/dist/pwa-192x192.png',
            vibrate: [200, 100, 200],
            requireInteraction: false,
            ...options
        }

        // Use service worker if available (better for PWAs)
        if (serviceWorkerRegistration.value) {
            return serviceWorkerRegistration.value.showNotification(title, defaultOptions)
        }

        // Fallback to regular notification
        return new Notification(title, defaultOptions)
    }

    /**
     * Check if notifications are enabled
     * @returns {boolean}
     */
    function areNotificationsEnabled() {
        return isSupported.value && permission.value === 'granted'
    }

    /**
     * Get service worker registration
     */
    async function getServiceWorkerRegistration() {
        if ('serviceWorker' in navigator) {
            try {
                serviceWorkerRegistration.value = await navigator.serviceWorker.ready
            } catch (error) {
                console.error('Error getting service worker:', error)
            }
        }
    }

    /**
     * Subscribe to push notifications
     * @param {string} vapidPublicKey - VAPID public key
     * @returns {Promise<PushSubscription>}
     */
    async function subscribeToPush(vapidPublicKey) {
        if (!serviceWorkerRegistration.value) {
            await getServiceWorkerRegistration()
        }

        if (!serviceWorkerRegistration.value) {
            throw new Error('Service worker not available')
        }

        try {
            const subscription = await serviceWorkerRegistration.value.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
            })

            return subscription
        } catch (error) {
            console.error('Error subscribing to push:', error)
            throw error
        }
    }

    /**
     * Unsubscribe from push notifications
     */
    async function unsubscribeFromPush() {
        if (!serviceWorkerRegistration.value) {
            return
        }

        try {
            const subscription = await serviceWorkerRegistration.value.pushManager.getSubscription()
            if (subscription) {
                await subscription.unsubscribe()
            }
        } catch (error) {
            console.error('Error unsubscribing from push:', error)
            throw error
        }
    }

    /**
     * Convert base64 VAPID key to Uint8Array
     * @private
     */
    function urlBase64ToUint8Array(base64String) {
        const padding = '='.repeat((4 - base64String.length % 4) % 4)
        const base64 = (base64String + padding)
            .replace(/\-/g, '+')
            .replace(/_/g, '/')

        const rawData = window.atob(base64)
        const outputArray = new Uint8Array(rawData.length)

        for (let i = 0; i < rawData.length; ++i) {
            outputArray[i] = rawData.charCodeAt(i)
        }
        return outputArray
    }

    // Initialize service worker on mount
    onMounted(() => {
        getServiceWorkerRegistration()
    })

    // Update permission when it changes
    onMounted(() => {
        if (isSupported.value) {
            // Check permission periodically
            const interval = setInterval(() => {
                permission.value = Notification.permission
            }, 1000)

            onUnmounted(() => {
                clearInterval(interval)
            })
        }
    })

    return {
        // State
        permission,
        isSupported,
        serviceWorkerRegistration,

        // Methods
        requestPermission,
        showNotification,
        areNotificationsEnabled,
        subscribeToPush,
        unsubscribeFromPush
    }
}
