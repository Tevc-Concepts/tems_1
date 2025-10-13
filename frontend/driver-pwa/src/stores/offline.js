import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import frappeClient from '@/utils/frappeClient'

export const useOfflineStore = defineStore('offline', () => {
  const isOnline = ref(navigator.onLine)
  const pendingSync = ref(0)
  const lastSyncTime = ref(null)
  const syncInProgress = ref(false)

  const hasPendingChanges = computed(() => pendingSync.value > 0)

  function initializeOnlineListener() {
    window.addEventListener('online', handleOnline)
    window.addEventListener('offline', handleOffline)
    
    // Check pending queue on init
    updatePendingCount()
  }

  function handleOnline() {
    isOnline.value = true
    syncOfflineData()
  }

  function handleOffline() {
    isOnline.value = false
  }

  async function syncOfflineData() {
    if (syncInProgress.value) return
    
    syncInProgress.value = true
    
    try {
      const result = await frappeClient.syncOfflineData()
      pendingSync.value = 0
      lastSyncTime.value = new Date()
      
      return result
    } catch (error) {
      console.error('Sync failed:', error)
      throw error
    } finally {
      syncInProgress.value = false
    }
  }

  async function updatePendingCount() {
    const count = await frappeClient.getPendingQueueCount()
    pendingSync.value = count
  }

  async function downloadOfflineData() {
    try {
      await frappeClient.call('tems.api.pwa.driver.get_offline_sync_data')
      lastSyncTime.value = new Date()
    } catch (error) {
      console.error('Failed to download offline data:', error)
      throw error
    }
  }

  return {
    isOnline,
    pendingSync,
    lastSyncTime,
    syncInProgress,
    hasPendingChanges,
    initializeOnlineListener,
    syncOfflineData,
    updatePendingCount,
    downloadOfflineData
  }
})