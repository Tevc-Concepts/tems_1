import { useOfflineStore } from '../stores/offline.js'
import { storeToRefs } from 'pinia'
import { onMounted } from 'vue'

/**
 * Offline sync composable
 * Manages offline queue and synchronization
 * 
 * @example
 * ```javascript
 * import { useOfflineSync } from '@shared/composables/useOfflineSync'
 * 
 * const { isOnline, hasPendingChanges, sync } = useOfflineSync()
 * 
 * // Initialize in App.vue
 * onMounted(() => {
 *   offlineSync.init()
 * })
 * 
 * // Manual sync
 * await sync()
 * ```
 */
export function useOfflineSync(options = {}) {
    const { autoInit = false } = options

    const offlineStore = useOfflineStore()

    const {
        isOnline,
        syncInProgress,
        lastSyncTime,
        queueCount,
        syncErrors,
        isSyncing,
        hasPendingChanges,
        lastSyncFormatted
    } = storeToRefs(offlineStore)

    // Auto-initialize if requested
    if (autoInit) {
        onMounted(() => {
            offlineStore.init()
        })
    }

    return {
        // State
        isOnline,
        syncInProgress,
        lastSyncTime,
        queueCount,
        syncErrors,
        isSyncing,
        hasPendingChanges,
        lastSyncFormatted,

        // Actions
        init: offlineStore.init,
        sync: offlineStore.syncOfflineData,
        updateQueueCount: offlineStore.updateQueueCount,
        clearCache: offlineStore.clearOfflineData,
        retryFailed: offlineStore.retryFailed
    }
}
