<template>
  <header class="bg-charcoal shadow-lg sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo and Title -->
        <div class="flex items-center space-x-3">
          <div class="flex-shrink-0">
            <img 
              v-if="logo" 
              :src="logo" 
              :alt="title" 
              class="h-10 w-auto"
            />
            <div v-else class="h-10 w-10 bg-neon-green rounded-lg flex items-center justify-center">
              <span class="text-charcoal font-bold text-xl">{{ titleInitial }}</span>
            </div>
          </div>
          <div class="hidden sm:block">
            <h1 class="text-xl font-bold text-white">{{ title }}</h1>
            <p v-if="subtitle" class="text-sm text-gray-400">{{ subtitle }}</p>
          </div>
        </div>

        <!-- Center Section (optional slot) -->
        <div class="flex-1 flex justify-center px-4">
          <slot name="center"></slot>
        </div>

        <!-- Right Section -->
        <div class="flex items-center space-x-4">
          <!-- Sync Status -->
          <div 
            v-if="showSyncStatus && hasPendingChanges" 
            class="hidden sm:flex items-center space-x-2 text-yellow-400"
          >
            <svg class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <span class="text-sm">{{ queueCount }} pending</span>
          </div>

          <!-- Online/Offline Indicator -->
          <div 
            v-if="showOnlineStatus" 
            :class="[
              'w-3 h-3 rounded-full',
              isOnline ? 'bg-neon-green' : 'bg-red-500'
            ]"
            :title="isOnline ? 'Online' : 'Offline'"
          ></div>

          <!-- Custom Actions Slot -->
          <slot name="actions"></slot>

          <!-- User Menu -->
          <div v-if="showUserMenu && isAuthenticated" class="relative">
            <button
              @click="toggleUserMenu"
              class="flex items-center space-x-2 text-white hover:text-neon-green transition-colors"
            >
              <div class="w-10 h-10 rounded-full bg-neon-green flex items-center justify-center text-charcoal font-semibold">
                {{ userInitials }}
              </div>
              <svg class="w-4 h-4 hidden sm:block" :class="{ 'rotate-180': isUserMenuOpen }" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
              </svg>
            </button>

            <!-- Dropdown Menu -->
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div
                v-if="isUserMenuOpen"
                class="absolute right-0 mt-2 w-56 rounded-md shadow-lg bg-white ring-1 ring-black ring-opacity-5"
              >
                <div class="py-1">
                  <!-- User Info -->
                  <div class="px-4 py-3 border-b border-gray-200">
                    <p class="text-sm font-medium text-gray-900">{{ userName }}</p>
                    <p v-if="user?.email" class="text-xs text-gray-500">{{ user.email }}</p>
                  </div>

                  <!-- Menu Items -->
                  <slot name="menu-items">
                    <a
                      href="#"
                      class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      @click.prevent="handleProfile"
                    >
                      Profile
                    </a>
                    <a
                      href="#"
                      class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100"
                      @click.prevent="handleSettings"
                    >
                      Settings
                    </a>
                  </slot>

                  <!-- Logout -->
                  <div class="border-t border-gray-200">
                    <button
                      @click="handleLogout"
                      class="block w-full text-left px-4 py-2 text-sm text-red-600 hover:bg-gray-100"
                    >
                      Logout
                    </button>
                  </div>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useAuth } from '../../composables/useAuth.js'
import { useOfflineSync } from '../../composables/useOfflineSync.js'

const props = defineProps({
  title: {
    type: String,
    default: 'TEMS'
  },
  subtitle: {
    type: String,
    default: ''
  },
  logo: {
    type: String,
    default: ''
  },
  showUserMenu: {
    type: Boolean,
    default: true
  },
  showOnlineStatus: {
    type: Boolean,
    default: true
  },
  showSyncStatus: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['logout', 'profile', 'settings'])

// Composables
const { user, isAuthenticated, userName, userInitials, logout } = useAuth()
const { isOnline, queueCount, hasPendingChanges } = useOfflineSync()

// Local state
const isUserMenuOpen = ref(false)

// Computed
const titleInitial = computed(() => {
  return props.title.charAt(0).toUpperCase()
})

// Methods
function toggleUserMenu() {
  isUserMenuOpen.value = !isUserMenuOpen.value
}

function closeUserMenu() {
  isUserMenuOpen.value = false
}

async function handleLogout() {
  closeUserMenu()
  await logout()
  emit('logout')
}

function handleProfile() {
  closeUserMenu()
  emit('profile')
}

function handleSettings() {
  closeUserMenu()
  emit('settings')
}

// Close menu when clicking outside
function handleClickOutside(event) {
  const userMenu = event.target.closest('.relative')
  if (!userMenu) {
    closeUserMenu()
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Additional custom styles if needed */
</style>
