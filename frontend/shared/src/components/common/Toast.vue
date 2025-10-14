<template>
  <teleport to="body">
    <transition-group
      name="toast"
      tag="div"
      class="fixed top-4 right-4 z-50 space-y-2 pointer-events-none"
    >
      <div
        v-for="toast in toasts"
        :key="toast.id"
        :class="toastClasses(toast)"
        class="pointer-events-auto"
        @click="handleDismiss(toast.id)"
      >
        <div class="flex items-start space-x-3 p-4">
          <!-- Icon -->
          <div class="flex-shrink-0">
            <svg v-if="toast.type === 'success'" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
            </svg>
            <svg v-else-if="toast.type === 'error'" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd"/>
            </svg>
            <svg v-else-if="toast.type === 'warning'" class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd"/>
            </svg>
            <svg v-else class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clip-rule="evenodd"/>
            </svg>
          </div>

          <!-- Message -->
          <div class="flex-1 pt-0.5">
            <p class="text-sm font-medium">{{ toast.message }}</p>
          </div>

          <!-- Close Button -->
          <button
            type="button"
            @click.stop="handleDismiss(toast.id)"
            class="flex-shrink-0 text-current opacity-70 hover:opacity-100 transition-opacity"
          >
            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>
        </div>

        <!-- Progress Bar (optional) -->
        <div
          v-if="toast.duration > 0"
          class="h-1 bg-white bg-opacity-30 rounded-b"
        >
          <div
            class="h-full bg-white bg-opacity-50 rounded-b transition-all"
            :style="{ width: getProgress(toast) + '%' }"
          ></div>
        </div>
      </div>
    </transition-group>
  </teleport>
</template>

<script setup>
import { computed } from 'vue'
import { useToast } from '../../composables/useToast.js'

// Get toasts from composable
const { toasts, dismiss } = useToast()

// Methods
function toastClasses(toast) {
  const baseClasses = [
    'rounded-lg shadow-lg max-w-sm w-full transform transition-all duration-300 cursor-pointer',
    'hover:scale-105'
  ]

  const typeClasses = {
    success: 'bg-green-600 text-white',
    error: 'bg-red-600 text-white',
    warning: 'bg-yellow-500 text-gray-900',
    info: 'bg-blue-600 text-white'
  }

  return [...baseClasses, typeClasses[toast.type] || typeClasses.info].join(' ')
}

function handleDismiss(toastId) {
  dismiss(toastId)
}

function getProgress(toast) {
  // Calculate progress based on time elapsed
  const now = Date.now()
  const elapsed = now - toast.timestamp
  const duration = toast.duration || 3000
  const remaining = Math.max(0, duration - elapsed)
  return (remaining / duration) * 100
}
</script>

<style scoped>
/* Toast animations */
.toast-enter-active,
.toast-leave-active {
  transition: all 0.3s ease;
}

.toast-enter-from {
  opacity: 0;
  transform: translateX(100%) scale(0.8);
}

.toast-enter-to {
  opacity: 1;
  transform: translateX(0) scale(1);
}

.toast-leave-from {
  opacity: 1;
  transform: translateX(0) scale(1);
}

.toast-leave-to {
  opacity: 0;
  transform: translateX(100%) scale(0.8);
}

/* Move animation for remaining toasts */
.toast-move {
  transition: transform 0.3s ease;
}
</style>
