import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import frappeClient from '../utils/frappeClient.js'

/**
 * Offline sync store
 * Manages offline queue and synchronization
 */
export const useOfflineStore = defineStore('offline', () => {
    const isOnline = ref(navigator.onLine)
    const syncInProgress = ref(false)
    const lastSyncTime = ref(null)
    const queueCount = ref(0)
    const syncErrors = ref([])

    const isSyncing = computed(() => syncInProgress.value)
    const hasPendingChanges = computed(() => queueCount.value > 0)
    const lastSyncFormatted = computed(() => {
        if (!lastSyncTime.value) return 'Never'
        const diff = Date.now() - lastSyncTime.value
        const minutes = Math.floor(diff / 60000)
        if (minutes < 1) return 'Just now'
        if (minutes === 1) return '1 minute ago'
        if (minutes < 60) return `${minutes} minutes ago`
        const hours = Math.floor(minutes / 60)
        if (hours === 1) return '1 hour ago'
        if (hours < 24) return `${hours} hours ago`
        const days = Math.floor(hours / 24)
        return days === 1 ? '1 day ago' : `${days} days ago`
    })

    /**
     * Initialize offline monitoring
     */
    function init() {
        // Update online status
        window.addEventListener('online', () => {
            isOnline.value = true
            syncOfflineData()
        })

        window.addEventListener('offline', () => {
            isOnline.value = false
        })

        // Update queue count
        updateQueueCount()

        // Auto-sync every 5 minutes if online
        setInterval(() => {
            if (isOnline.value && !syncInProgress.value) {
                syncOfflineData()
            }
        }, 5 * 60 * 1000)
    }

    /**
     * Update queue count
     */
    async function updateQueueCount() {
        try {
            queueCount.value = await frappeClient.getPendingQueueCount()
        } catch (error) {
            console.error('Failed to update queue count:', error)
        }
    }

    /**
     * Sync offline data
     */
    async function syncOfflineData() {
        if (syncInProgress.value || !isOnline.value) return

        syncInProgress.value = true
        syncErrors.value = []

        try {
            const result = await frappeClient.syncOfflineData()

            if (result.synced > 0) {
                console.log(`Synced ${result.synced} offline changes`)
                lastSyncTime.value = Date.now()
            }

            if (result.failed && result.failed.length > 0) {
                syncErrors.value = result.failed
                console.error('Some items failed to sync:', result.failed)
            }

            await updateQueueCount()

            return result
        } catch (error) {
            console.error('Sync failed:', error)
            syncErrors.value.push({ error: error.message })
        } finally {
            syncInProgress.value = false
        }
    }

    /**
     * Clear all offline data
     */
    async function clearOfflineData() {
        try {
            await frappeClient.clearCache()
            queueCount.value = 0
            syncErrors.value = []
            lastSyncTime.value = null
        } catch (error) {
            console.error('Failed to clear offline data:', error)
            throw error
        }
    }

    /**
     * Retry failed sync items
     */
    async function retryFailed() {
        return syncOfflineData()
    }

    return {
        isOnline,
        syncInProgress,
        lastSyncTime,
        queueCount,
        syncErrors,
        isSyncing,
        hasPendingChanges,
        lastSyncFormatted,
        init,
        updateQueueCount,
        syncOfflineData,
        clearOfflineData,
        retryFailed
    }
})
