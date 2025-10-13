<template>
  <transition name="slide-up">
    <div 
      v-if="!offlineStore.isOnline"
      class="fixed bottom-20 left-4 right-4 bg-amber-500 text-white px-4 py-3 rounded-lg shadow-lg z-50 flex items-center justify-between"
    >
      <div class="flex items-center space-x-2">
        <WifiOff class="w-5 h-5" />
        <div>
          <p class="font-medium text-sm">You're offline</p>
          <p class="text-xs text-amber-100">Changes will sync when online</p>
        </div>
      </div>
      
      <div 
        v-if="offlineStore.hasPendingChanges"
        class="bg-white text-amber-600 px-2 py-1 rounded text-xs font-bold"
      >
        {{ offlineStore.pendingSync }} pending
      </div>
    </div>
  </transition>
</template>

<script setup>
import { WifiOff } from 'lucide-vue-next'
import { useOfflineStore } from '@/stores/offline'

const offlineStore = useOfflineStore()
</script>

<style scoped>
.slide-up-enter-active,
.slide-up-leave-active {
  transition: all 0.3s ease;
}

.slide-up-enter-from,
.slide-up-leave-to {
  transform: translateY(100px);
  opacity: 0;
}
</style>