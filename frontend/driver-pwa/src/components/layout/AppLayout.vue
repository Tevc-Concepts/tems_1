<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <AppHeader />
    
    <!-- Main Content -->
    <main class="flex-1 pb-20 safe-bottom">
      <div class="max-w-7xl mx-auto px-4 py-6">
        <router-view v-slot="{ Component }">
          <transition name="fade" mode="out-in">
            <component :is="Component" />
          </transition>
        </router-view>
      </div>
    </main>
    
    <!-- Bottom Navigation -->
    <AppBottomNav />
    
    <!-- SOS Emergency Button -->
    <SOSButton />
    
    <!-- Offline Indicator -->
    <OfflineIndicator />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppHeader from './AppHeader.vue'
import AppBottomNav from './AppBottomNav.vue'
import OfflineIndicator from '../common/OfflineIndicator.vue'
import SOSButton from '../common/SOSButton.vue'
import { useAuthStore } from '@/stores/auth'
import { useOfflineStore } from '@/stores/offline'

const authStore = useAuthStore()
const offlineStore = useOfflineStore()

onMounted(async () => {
  await authStore.fetchUserInfo()
  offlineStore.initializeOnlineListener()
})
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>