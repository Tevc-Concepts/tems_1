<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-emerald-50 to-emerald-100 dark:from-gray-900 dark:to-gray-800 px-4">
    <div class="max-w-md w-full space-y-8">
      <div class="text-center">
        <div class="flex justify-center mb-4">
          <img src="/logo.png" alt="TEMS Logo" class="h-16 w-16" />
        </div>
        <h2 class="text-4xl font-bold text-emerald-600 dark:text-emerald-400 mb-2">TEMS Fleet</h2>
        <p class="text-gray-600 dark:text-gray-400">Fleet Manager Access</p>
      </div>

      <form @submit.prevent="handleLogin" class="mt-8 space-y-6 bg-white dark:bg-gray-800 p-8 rounded-xl shadow-xl">
        <div class="space-y-4">
          <div>
            <label for="usr" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Username
            </label>
            <input
              id="usr"
              v-model="credentials.usr"
              type="text"
              required
              class="appearance-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 dark:bg-gray-700 sm:text-sm"
              placeholder="Enter your username"
            />
          </div>

          <div>
            <label for="pwd" class="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-1">
              Password
            </label>
            <input
              id="pwd"
              v-model="credentials.pwd"
              type="password"
              required
              class="appearance-none relative block w-full px-3 py-2 border border-gray-300 dark:border-gray-600 placeholder-gray-500 dark:placeholder-gray-400 text-gray-900 dark:text-white rounded-lg focus:outline-none focus:ring-emerald-500 focus:border-emerald-500 dark:bg-gray-700 sm:text-sm"
              placeholder="Enter your password"
            />
          </div>
        </div>

        <div v-if="error" class="text-red-600 dark:text-red-400 text-sm text-center">
          {{ error }}
        </div>

        <button
          type="submit"
          :disabled="loading"
          class="w-full flex justify-center py-3 px-4 border border-transparent rounded-lg shadow-sm text-sm font-medium text-white bg-emerald-600 hover:bg-emerald-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <span v-if="!loading">Sign In</span>
          <span v-else class="flex items-center">
            <svg class="animate-spin h-5 w-5 mr-2" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4" fill="none"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Signing in...
          </span>
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth, useToast } from '@shared'

const router = useRouter()
const { login } = useAuth()
const toast = useToast()

const credentials = ref({
  usr: '',
  pwd: ''
})

const loading = ref(false)
const error = ref(null)

async function handleLogin() {
  loading.value = true
  error.value = null

  try {
    await login(credentials.value.usr, credentials.value.pwd)
    toast.success('Login successful')
    router.push('/dashboard')
  } catch (err) {
    error.value = err.message || 'Invalid credentials'
    toast.error('Login failed')
  } finally {
    loading.value = false
  }
}
</script>
