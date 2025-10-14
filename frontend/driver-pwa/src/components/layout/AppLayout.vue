<template>
  <div class="min-h-screen flex flex-col bg-gray-50">
    <!-- Header -->
    <AppHeader 
      title="Driver Portal"
      :show-sync-status="true"
      @logout="handleLogout"
    />
    
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
    <AppBottomNav 
      :items="bottomNavItems"
      :current-route="$route.path"
      @navigate="handleNavigate"
    />
    
    <!-- SOS Emergency Button (Driver-specific) -->
    <SOSButton />
    
    <!-- Offline Indicator -->
    <OfflineIndicator />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { AppHeader, AppBottomNav } from '@shared'
import OfflineIndicator from '../common/OfflineIndicator.vue'
import SOSButton from '../common/SOSButton.vue'
import { Home, Route, Clipboard, AlertTriangle, User } from 'lucide-vue-next'

const router = useRouter()
const route = useRoute()

// Bottom navigation items
const bottomNavItems = computed(() => [
  {
    name: 'Home',
    href: '/driver',
    icon: Home
  },
  {
    name: 'Trips',
    href: '/driver/trips',
    icon: Route
  },
  {
    name: 'Inspect',
    href: '/driver/inspection',
    icon: Clipboard
  },
  {
    name: 'Incident',
    href: '/driver/incident',
    icon: AlertTriangle
  },
  {
    name: 'Profile',
    href: '/driver/profile',
    icon: User
  }
])

function handleNavigate(item) {
  router.push(item.href)
}

function handleLogout() {
  router.push('/login')
}
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