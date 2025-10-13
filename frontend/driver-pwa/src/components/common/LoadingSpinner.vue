<template>
  <div class="flex items-center justify-center" :class="containerClass">
    <div class="relative">
      <div 
        class="w-12 h-12 rounded-full border-4 border-gray-200 border-t-primary-600 animate-spin"
        :style="{ width: size, height: size }"
      />
      <p v-if="message" class="text-sm text-gray-600 mt-3 text-center">
        {{ message }}
      </p>
    </div>
  </div>
</template>

<script setup>
defineProps({
  size: {
    type: String,
    default: '3rem'
  },
  message: {
    type: String,
    default: ''
  },
  containerClass: {
    type: String,
    default: 'py-12'
  }
})
</script>