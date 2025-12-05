<template>
  <div class="min-h-screen bg-gray-50 flex flex-col">
    <!-- Top Navigation Bar -->
    <nav class="bg-white shadow-sm border-b border-gray-200">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex justify-between h-16">
          <div class="flex items-center space-x-3">
            <img src="/logo.png" alt="TEMS Logo" class="h-8 w-8" />
            <h1 class="text-xl font-bold text-emerald-600">TEMS Fleet</h1>
          </div>
          <!-- Desktop Navigation -->
          <div class="hidden md:flex items-center space-x-4">
            <router-link to="/dashboard" class="text-gray-700 hover:text-emerald-600 px-3 py-2 rounded-md text-sm font-medium">
              Dashboard
            </router-link>
            <router-link to="/assets" class="text-gray-700 hover:text-emerald-600 px-3 py-2 rounded-md text-sm font-medium">
              Assets
            </router-link>
            <router-link to="/maintenance" class="text-gray-700 hover:text-emerald-600 px-3 py-2 rounded-md text-sm font-medium">
              Maintenance
            </router-link>
            <router-link to="/fuel" class="text-gray-700 hover:text-emerald-600 px-3 py-2 rounded-md text-sm font-medium">
              Fuel
            </router-link>
            <button @click="handleLogout" class="text-gray-700 hover:text-emerald-600 px-3 py-2 rounded-md text-sm font-medium">
              Logout
            </button>
          </div>
          <!-- Mobile menu button -->
          <div class="md:hidden flex items-center">
            <button @click="mobileMenuOpen = !mobileMenuOpen" class="text-gray-700 hover:text-emerald-600 p-2">
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
          <router-link to="/dashboard" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-emerald-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
            Dashboard
          </router-link>
          <router-link to="/assets" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-emerald-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
            Assets
          </router-link>
          <router-link to="/maintenance" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-emerald-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
            Maintenance
          </router-link>
          <router-link to="/fuel" @click="mobileMenuOpen = false" class="block text-gray-700 hover:text-emerald-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
            Fuel
          </router-link>
          <button @click="handleLogout" class="block w-full text-left text-gray-700 hover:text-emerald-600 hover:bg-gray-50 px-3 py-2 rounded-md text-base font-medium">
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
