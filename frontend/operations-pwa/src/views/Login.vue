<template>
  <div class="min-h-screen flex items-center justify-center bg-gradient-to-br from-primary-50 to-primary-100 px-4">
    <div class="max-w-md w-full">
      <div class="text-center mb-8">
        <h1 class="text-4xl font-bold text-primary-700 mb-2">TEMS Operations</h1>
        <p class="text-gray-600">Fleet Tracking & Dispatch Management</p>
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
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
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
              class="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
              placeholder="Enter your password"
            />
          </div>

          <button
            type="submit"
            :disabled="loading"
            class="w-full bg-primary text-white py-3 rounded-lg font-medium hover:bg-primary-700 focus:outline-none focus:ring-4 focus:ring-primary-300 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            {{ loading ? 'Signing in...' : 'Sign In' }}
          </button>

          <div v-if="error" class="text-red-600 text-sm text-center">
            {{ error }}
          </div>
        </form>
      </div>

      <div class="mt-6 text-center text-sm text-gray-600">
        <p>Operations Manager Access Only</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuth, useToast } from '@shared'

const router = useRouter()
const { login } = useAuth()
const { showToast } = useToast()

const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref(null)

async function handleLogin() {
  loading.value = true
  error.value = null

  try {
    await login(username.value, password.value)
    showToast('Login successful', 'success')
    router.push({ name: 'Dashboard' })
  } catch (err) {
    error.value = err.message || 'Login failed. Please check your credentials.'
    showToast(error.value, 'error')
  } finally {
    loading.value = false
  }
}
</script>
