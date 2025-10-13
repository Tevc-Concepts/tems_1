import { ref, watch } from 'vue'
import { useOnline } from '@vueuse/core'

export function useNotifications() {
    const permission = ref(Notification.permission)
    const isSupported = 'Notification' in window
    const isOnline = useOnline()

    async function requestPermission() {
        if (!isSupported) {
            console.warn('Notifications not supported')
            return 'denied'
        }

        const result = await Notification.requestPermission()
        permission.value = result
        return result
    }

    function showNotification(title, options = {}) {
        if (permission.value !== 'granted') {
            console.warn('Notification permission not granted')
            return null
        }

        const defaultOptions = {
            icon: '/assets/tems/frontend/driver-pwa/dist/pwa-192x192.png',
            badge: '/assets/tems/frontend/driver-pwa/dist/pwa-192x192.png',
            vibrate: [200, 100, 200],
            ...options
        }

        if ('serviceWorker' in navigator && navigator.serviceWorker.controller) {
            // Use service worker to show notification (works in background)
            return navigator.serviceWorker.ready.then((registration) => {
                return registration.showNotification(title, defaultOptions)
            })
        } else {
            // Fallback to regular notification
            return new Notification(title, defaultOptions)
        }
    }

    // Show notification when offline data is synced
    watch(isOnline, (online) => {
        if (online) {
            showNotification('Back Online', {
                body: 'You are back online. Syncing data...',
                tag: 'online-status'
            })
        }
    })

    return {
        permission,
        isSupported,
        requestPermission,
        showNotification
    }
}

// Push notification subscription
export function usePushNotifications() {
    const subscription = ref(null)
    const isSubscribed = ref(false)

    async function subscribe(vapidPublicKey) {
        if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
            throw new Error('Push notifications not supported')
        }

        try {
            const registration = await navigator.serviceWorker.ready

            const sub = await registration.pushManager.subscribe({
                userVisibleOnly: true,
                applicationServerKey: urlBase64ToUint8Array(vapidPublicKey)
            })

            subscription.value = sub
            isSubscribed.value = true

            return sub
        } catch (error) {
            console.error('Failed to subscribe to push notifications:', error)
            throw error
        }
    }

    async function unsubscribe() {
        if (!subscription.value) return

        try {
            await subscription.value.unsubscribe()
            subscription.value = null
            isSubscribed.value = false
        } catch (error) {
            console.error('Failed to unsubscribe:', error)
            throw error
        }
    }

    async function checkSubscription() {
        if (!('serviceWorker' in navigator) || !('PushManager' in window)) {
            return null
        }

        try {
            const registration = await navigator.serviceWorker.ready
            const sub = await registration.pushManager.getSubscription()

            subscription.value = sub
            isSubscribed.value = !!sub

            return sub
        } catch (error) {
            console.error('Failed to check subscription:', error)
            return null
        }
    }

    return {
        subscription,
        isSubscribed,
        subscribe,
        unsubscribe,
        checkSubscription
    }
}

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
