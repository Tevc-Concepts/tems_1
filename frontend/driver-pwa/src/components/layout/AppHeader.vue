<template>
  <header class="sticky top-0 z-50 bg-gradient-to-r from-primary-600 to-primary-500 text-white shadow-lg">
    <div class="max-w-7xl mx-auto px-4">
      <div class="flex items-center justify-between h-16">
        <!-- Logo & Title -->
        <div class="flex items-center space-x-3">
          <div class="w-10 h-10 bg-white rounded-lg flex items-center justify-center shadow-md">
            <Truck class="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h1 class="text-lg font-bold">TEMS Driver</h1>
            <p class="text-xs text-primary-100">{{ pageTitle }}</p>
          </div>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center space-x-3">
          <!-- Sync Status -->
          <button 
            v-if="offlineStore.hasPendingChanges"
            @click="handleSync"
            class="p-2 rounded-lg bg-white/20 hover:bg-white/30 transition-colors"
            :disabled="offlineStore.syncInProgress"
          >
            <RefreshCw 
              :class="['w-5 h-5', offlineStore.syncInProgress && 'animate-spin']" 
            />
          </button>
          
          <!-- Profile -->
          <button 
            @click="showProfile = !showProfile"
            class="flex items-center space-x-2 p-2 rounded-lg hover:bg-white/20 transition-colors"
          >
            <div class="w-8 h-8 bg-white rounded-full flex items-center justify-center">
              <User class="w-5 h-5 text-primary-600" />
            </div>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Profile Dropdown -->
    <transition name="slide-down">
      <div 
        v-if="showProfile"
        class="absolute right-4 top-20 w-64 bg-white rounded-xl shadow-2xl overflow-hidden z-50"
      >
        <div class="p-4 bg-gradient-to-br from-primary-50 to-white border-b">
          <p class="font-semibold text-gray-900">{{ authStore.driverName }}</p>
          <p class="text-sm text-gray-600">{{ authStore.user?.email }}</p>
        </div>
        
        <div class="p-2">
          <router-link
            to="/driver/profile"
            class="flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-gray-50 transition-colors text-gray-700"
            @click="showProfile = false"
          >
            <UserCircle class="w-5 h-5" />
            <span>My Profile</span>
          </router-link>
          
          <button
            @click="handleLogout"
            class="w-full flex items-center space-x-3 px-4 py-3 rounded-lg hover:bg-red-50 transition-colors text-red-600"
          >
            <LogOut class="w-5 h-5" />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </transition>
  </header>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRoute } from 'vue-router'
import { Truck, User, UserCircle, LogOut, RefreshCw } from 'lucide-vue-next'
import { useAuthStore } from '@/stores/auth'
import { useOfflineStore } from '@/stores/offline'

const route = useRoute()
const authStore = useAuthStore()
const offlineStore = useOfflineStore()
const showProfile = ref(false)

const pageTitle = computed(() => route.meta.title || 'Dashboard')

async function handleSync() {
  try {
    await offlineStore.syncOfflineData()
    // Show success notification
  } catch (error) {
    console.error('Sync failed:', error)
  }
}

async function handleLogout() {
  await authStore.logout()
}
</script>

<style scoped>
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.2s ease;
}

.slide-down-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.slide-down-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}
</style>