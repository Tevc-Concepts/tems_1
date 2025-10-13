<template>
  <div class="space-y-6">
    <!-- Header -->
    <div class="card p-4">
      <h2 class="text-xl font-bold text-gray-900 mb-2">Settings</h2>
      <p class="text-sm text-gray-600">Manage your app preferences</p>
    </div>

    <!-- Sync Status -->
    <div class="card p-4">
      <div class="flex items-center justify-between mb-4">
        <h3 class="font-semibold text-gray-900">Offline Data</h3>
        <StatusBadge :status="offlineStore.isOnline ? 'Online' : 'Offline'" />
      </div>

      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p class="text-sm font-medium text-gray-900">Pending Sync</p>
            <p class="text-xs text-gray-600">Data waiting to be uploaded</p>
          </div>
          <span class="text-lg font-bold text-primary-600">{{ offlineStore.pendingSync }}</span>
        </div>

        <div v-if="offlineStore.lastSyncTime" class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p class="text-sm font-medium text-gray-900">Last Sync</p>
            <p class="text-xs text-gray-600">{{ formatLastSync }}</p>
          </div>
          <CheckCircle class="w-5 h-5 text-green-600" />
        </div>

        <button
          @click="syncOfflineData"
          class="w-full btn-primary py-3"
          :disabled="!offlineStore.isOnline || offlineStore.syncInProgress"
        >
          <RefreshCw class="w-5 h-5 mr-2" :class="{ 'animate-spin': offlineStore.syncInProgress }" />
          {{ offlineStore.syncInProgress ? 'Syncing...' : 'Sync Now' }}
        </button>

        <button
          @click="downloadOfflineData"
          class="w-full btn-secondary py-3"
          :disabled="!offlineStore.isOnline || downloading"
        >
          <Download class="w-5 h-5 mr-2" :class="{ 'animate-spin': downloading }" />
          {{ downloading ? 'Downloading...' : 'Download for Offline Use' }}
        </button>
      </div>
    </div>

    <!-- Notification Settings -->
    <div class="card p-4">
      <h3 class="font-semibold text-gray-900 mb-4">Notifications</h3>

      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p class="text-sm font-medium text-gray-900">Push Notifications</p>
            <p class="text-xs text-gray-600">Receive alerts and updates</p>
          </div>
          <button
            @click="toggleNotifications"
            class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors"
            :class="notificationsEnabled ? 'bg-primary-600' : 'bg-gray-200'"
          >
            <span
              class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
              :class="notificationsEnabled ? 'translate-x-6' : 'translate-x-1'"
            ></span>
          </button>
        </div>

        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p class="text-sm font-medium text-gray-900">Sound Alerts</p>
            <p class="text-xs text-gray-600">Play sound for notifications</p>
          </div>
          <button
            @click="soundEnabled = !soundEnabled"
            class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors"
            :class="soundEnabled ? 'bg-primary-600' : 'bg-gray-200'"
          >
            <span
              class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
              :class="soundEnabled ? 'translate-x-6' : 'translate-x-1'"
            ></span>
          </button>
        </div>

        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p class="text-sm font-medium text-gray-900">Vibration</p>
            <p class="text-xs text-gray-600">Vibrate for important alerts</p>
          </div>
          <button
            @click="vibrationEnabled = !vibrationEnabled"
            class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors"
            :class="vibrationEnabled ? 'bg-primary-600' : 'bg-gray-200'"
          >
            <span
              class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
              :class="vibrationEnabled ? 'translate-x-6' : 'translate-x-1'"
            ></span>
          </button>
        </div>
      </div>
    </div>

    <!-- Location Settings -->
    <div class="card p-4">
      <h3 class="font-semibold text-gray-900 mb-4">Location</h3>

      <div class="space-y-3">
        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p class="text-sm font-medium text-gray-900">Location Tracking</p>
            <p class="text-xs text-gray-600">Track location during trips</p>
          </div>
          <button
            @click="locationEnabled = !locationEnabled"
            class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors"
            :class="locationEnabled ? 'bg-primary-600' : 'bg-gray-200'"
          >
            <span
              class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
              :class="locationEnabled ? 'translate-x-6' : 'translate-x-1'"
            ></span>
          </button>
        </div>

        <div class="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
          <div>
            <p class="text-sm font-medium text-gray-900">High Accuracy Mode</p>
            <p class="text-xs text-gray-600">Use GPS for precise location</p>
          </div>
          <button
            @click="highAccuracyMode = !highAccuracyMode"
            class="relative inline-flex h-6 w-11 items-center rounded-full transition-colors"
            :class="highAccuracyMode ? 'bg-primary-600' : 'bg-gray-200'"
          >
            <span
              class="inline-block h-4 w-4 transform rounded-full bg-white transition-transform"
              :class="highAccuracyMode ? 'translate-x-6' : 'translate-x-1'"
            ></span>
          </button>
        </div>
      </div>
    </div>

    <!-- App Info -->
    <div class="card p-4">
      <h3 class="font-semibold text-gray-900 mb-4">App Information</h3>

      <div class="space-y-2 text-sm">
        <div class="flex justify-between">
          <span class="text-gray-600">Version</span>
          <span class="font-medium text-gray-900">1.0.0</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-600">Build</span>
          <span class="font-medium text-gray-900">{{ buildNumber }}</span>
        </div>
        <div class="flex justify-between">
          <span class="text-gray-600">Last Updated</span>
          <span class="font-medium text-gray-900">Oct 2025</span>
        </div>
      </div>
    </div>

    <!-- Cache Management -->
    <div class="card p-4">
      <h3 class="font-semibold text-gray-900 mb-4">Storage</h3>

      <button
        @click="clearCache"
        class="w-full btn-secondary py-3 text-red-600 hover:bg-red-50"
      >
        <Trash2 class="w-5 h-5 mr-2" />
        Clear Cache
      </button>
    </div>

    <!-- Logout -->
    <div class="card p-4">
      <button
        @click="logout"
        class="w-full btn-secondary py-3 text-red-600 hover:bg-red-50"
      >
        <LogOut class="w-5 h-5 mr-2" />
        Logout
      </button>
    </div>

    <!-- Toast -->
    <Toast
      v-model="showToast"
      :type="toastType"
      :title="toastTitle"
      :message="toastMessage"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { formatDistanceToNow } from 'date-fns'
import { 
  RefreshCw, Download, CheckCircle, Trash2, LogOut 
} from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { useOfflineStore } from '@/stores/offline'
import { useNotifications } from '@/composables/useNotifications'
import StatusBadge from '@/components/common/StatusBadge.vue'
import Toast from '@/components/common/Toast.vue'

const authStore = useAuthStore()
const offlineStore = useOfflineStore()
const { permission, requestPermission } = useNotifications()

const downloading = ref(false)
const showToast = ref(false)
const toastType = ref('success')
const toastTitle = ref('')
const toastMessage = ref('')

const notificationsEnabled = ref(permission.value === 'granted')
const soundEnabled = ref(true)
const vibrationEnabled = ref(true)
const locationEnabled = ref(true)
const highAccuracyMode = ref(true)
const buildNumber = ref('20251013')

const formatLastSync = computed(() => {
  if (!offlineStore.lastSyncTime) return 'Never'
  try {
    return formatDistanceToNow(offlineStore.lastSyncTime, { addSuffix: true })
  } catch (e) {
    return 'Unknown'
  }
})

async function syncOfflineData() {
  try {
    const result = await offlineStore.syncOfflineData()
    
    toastType.value = 'success'
    toastTitle.value = 'Sync Complete'
    toastMessage.value = `Synced ${result.synced} items successfully`
    showToast.value = true
  } catch (error) {
    toastType.value = 'error'
    toastTitle.value = 'Sync Failed'
    toastMessage.value = error.message || 'Failed to sync data'
    showToast.value = true
  }
}

async function downloadOfflineData() {
  downloading.value = true
  
  try {
    await offlineStore.downloadOfflineData()
    
    toastType.value = 'success'
    toastTitle.value = 'Download Complete'
    toastMessage.value = 'Offline data downloaded successfully'
    showToast.value = true
  } catch (error) {
    toastType.value = 'error'
    toastTitle.value = 'Download Failed'
    toastMessage.value = error.message || 'Failed to download data'
    showToast.value = true
  } finally {
    downloading.value = false
  }
}

async function toggleNotifications() {
  if (!notificationsEnabled.value) {
    const result = await requestPermission()
    notificationsEnabled.value = result === 'granted'
    
    if (!notificationsEnabled.value) {
      toastType.value = 'warning'
      toastTitle.value = 'Permission Denied'
      toastMessage.value = 'Enable notifications in browser settings'
      showToast.value = true
    }
  } else {
    notificationsEnabled.value = false
  }
}

async function clearCache() {
  if (confirm('Are you sure you want to clear all cached data? This cannot be undone.')) {
    try {
      // Clear cache via frappe client
      const frappeClient = (await import('@/utils/frappeClient')).default
      await frappeClient.clearCache()
      
      toastType.value = 'success'
      toastTitle.value = 'Cache Cleared'
      toastMessage.value = 'All cached data has been cleared'
      showToast.value = true
    } catch (error) {
      toastType.value = 'error'
      toastTitle.value = 'Error'
      toastMessage.value = 'Failed to clear cache'
      showToast.value = true
    }
  }
}

async function logout() {
  if (confirm('Are you sure you want to logout?')) {
    await authStore.logout()
  }
}

onMounted(() => {
  // Load saved preferences from localStorage
  const prefs = localStorage.getItem('driver_app_prefs')
  if (prefs) {
    const parsed = JSON.parse(prefs)
    soundEnabled.value = parsed.soundEnabled ?? true
    vibrationEnabled.value = parsed.vibrationEnabled ?? true
    locationEnabled.value = parsed.locationEnabled ?? true
    highAccuracyMode.value = parsed.highAccuracyMode ?? true
  }
})

// Watch and save preferences
import { watch } from 'vue'
watch(
  [soundEnabled, vibrationEnabled, locationEnabled, highAccuracyMode],
  () => {
    localStorage.setItem('driver_app_prefs', JSON.stringify({
      soundEnabled: soundEnabled.value,
      vibrationEnabled: vibrationEnabled.value,
      locationEnabled: locationEnabled.value,
      highAccuracyMode: highAccuracyMode.value
    }))
  }
)
</script>
