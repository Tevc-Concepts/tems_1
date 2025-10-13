<template>
  <nav class="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 safe-bottom z-40">
    <div class="max-w-7xl mx-auto px-2">
      <div class="flex justify-around items-center h-16">
        <router-link
          v-for="item in navItems"
          :key="item.name"
          :to="item.path"
          class="flex flex-col items-center justify-center flex-1 py-2 px-1 rounded-lg transition-all duration-200"
          :class="isActive(item.path) ? 'text-primary-600' : 'text-gray-500 hover:text-gray-700'"
        >
          <component 
            :is="item.icon" 
            :class="['w-6 h-6 mb-1 transition-transform', isActive(item.path) && 'scale-110']"
          />
          <span class="text-xs font-medium">{{ item.label }}</span>
          <div 
            v-if="isActive(item.path)"
            class="absolute bottom-0 w-12 h-1 bg-primary-600 rounded-t-full"
          />
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import { 
  LayoutDashboard, 
  MapPin, 
  ClipboardCheck, 
  AlertTriangle,
  User 
} from 'lucide-vue-next'

const route = useRoute()

const navItems = [
  {
    name: 'dashboard',
    label: 'Dashboard',
    path: '/driver',
    icon: LayoutDashboard
  },
  {
    name: 'trips',
    label: 'Trips',
    path: '/driver/trips',
    icon: MapPin
  },
  {
    name: 'inspection',
    label: 'Inspect',
    path: '/driver/inspection',
    icon: ClipboardCheck
  },
  {
    name: 'incident',
    label: 'Incident',
    path: '/driver/incident',
    icon: AlertTriangle
  },
  {
    name: 'profile',
    label: 'Profile',
    path: '/driver/profile',
    icon: User
  }
]

function isActive(path) {
  if (path === '/driver') {
    return route.path === path
  }
  return route.path.startsWith(path)
}
</script>