<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Top Navigation Bar -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center space-x-3">
            <img src="/logo.png" alt="TEMS Logo" class="h-8 w-8" />
            <h1 class="text-xl font-bold text-blue-600">TEMS Driver</h1>
          </div>
          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center space-x-4">
            <router-link to="/" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Dashboard
            </router-link>
            <router-link to="/trips" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Trips
            </router-link>
            <router-link to="/inspection" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Inspection
            </router-link>
            <router-link to="/incident" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Incident
            </router-link>
            <router-link to="/profile" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Profile
            </router-link>
            <button @click="handleLogout" class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium">
              Logout
            </button>
          </div>
          <!-- Mobile menu button -->
          <div class="md:hidden flex items-center">
            <button @click="mobileMenuOpen = !mobileMenuOpen" class="text-gray-700 hover:text-blue-600 p-2">
              <svg v-if="!mobileMenuOpen" class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
              <svg v-else class="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
      <!-- Mobile menu -->
      <div v-if="mobileMenuOpen" class="md:hidden border-t border-gray-200">
        <div class="px-2 pt-2 pb-3 space-y-1">
          <router-link to="/" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
            Dashboard
          </router-link>
          <router-link to="/trips" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
            Trips
          </router-link>
          <router-link to="/inspection" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
            Inspection
          </router-link>
          <router-link to="/incident" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
            Incident
          </router-link>
          <router-link to="/profile" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
            Profile
          </router-link>
          <button @click="handleLogout" class="block w-full text-left text-gray-700 hover:text-blue-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
            Logout
          </button>
        </div>
      </div>
    </nav>

    <!-- Main Content Area -->
    <main class="flex-1">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@shared'

const router = useRouter()
const authStore = useAuthStore()
const mobileMenuOpen = ref(false)

function handleLogout() {
  authStore.logout()
  router.push('/login')
  mobileMenuOpen.value = false
}
</script>
