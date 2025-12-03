<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-blue-100 px-4">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <div class="inline-block p-4 bg-white rounded-full shadow-lg mb-4">
          <svg class="w-16 h-16 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <h1 class="text-4xl font-bold text-blue-700 mb-2">TEMS Driver</h1>
        <p class="text-gray-600">Transport Excellence Management System</p>
      </div>

      <div class="bg-white rounded-lg shadow-lg p-8">
        <form @submit.prevent="handleLogin" class="space-y-6">
          <div>
            <label for="username" class="block text-sm font-medium text-gray-700 mb-2">
              Username
            </label>
            <input
              id="username"
              v-model="username"
              type="text"
              required
              autocomplete="username"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter your username"
            />
          </div>

          <div>
            <label for="password" class="block text-sm font-medium text-gray-700 mb-2">
              Password
            </label>
            <input
              id="password"
              v-model="password"
              type="password"
              required
              autocomplete="current-password"
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
              placeholder="Enter your password"
            />
          </div>

          <div class="flex items-center">
            <input
              id="remember"
              v-model="remember"
              type="checkbox"
              class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
            />
            <label for="remember" class="ml-2 block text-sm text-gray-700">
              Remember me
            </label>
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-blue-600 text-white py-3 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-4 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <span v-if="loading" class="flex items-center justify-center">
              <svg class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              Signing in...
            </span>
            <span v-else>Sign In</span>
          </button>

          <div v-if="error" class="p-3 bg-red-50 border border-red-200 rounded-lg">
            <p class="text-red-600 text-sm text-center">{{ error }}</p>
          </div>
        </form>
      </div>

      <div class="mt-6 text-center text-sm text-gray-600">
        <p>Driver Portal Access</p>
        <p class="mt-2">Need help? Contact your fleet manager</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuth } from '@shared'

const router = useRouter()
const route = useRoute()
const { login, isAuthenticated } = useAuth()

const username = ref('')
const password = ref('')
const remember = ref(false)
const loading = ref(false)
const error = ref(null)

// If already authenticated, redirect to dashboard
onMounted(() => {
  if (isAuthenticated.value) {
    const redirect = route.query.redirect || '/driver'
    router.push(redirect)
  }
})

async function handleLogin() {
  loading.value = true
  error.value = null

  try {
    await login(username.value, password.value)
    
    // Get redirect URL from query or default to dashboard
    const redirect = route.query.redirect || '/driver'
    
    // Use router.push for internal navigation
    router.push(redirect)
  } catch (err) {
    console.error('Login error:', err)
    error.value = err.message || 'Login failed. Please check your credentials and try again.'
  } finally {
    loading.value = false
  }
}
</script>
