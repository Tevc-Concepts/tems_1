<template>
  <div class="flex flex-col items-center justify-center py-12 px-4 text-center">
    <div class="w-20 h-20 bg-gray-100 rounded-full flex items-center justify-center mb-4">
      <component :is="icon" class="w-10 h-10 text-gray-400" />
    </div>
    <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ title }}</h3>
    <p class="text-sm text-gray-600 mb-6 max-w-sm">{{ message }}</p>
    <button 
      v-if="actionLabel"
      @click="$emit('action')"
      class="btn-primary"
    >
      {{ actionLabel }}
    </button>
  </div>
</template>

<script setup>
import { Inbox } from 'lucide-vue-next'

defineProps({
  icon: {
    type: Object,
    default: () => Inbox
  },
  title: {
    type: String,
    default: 'No items found'
  },
  message: {
    type: String,
    default: 'There are no items to display at the moment.'
  },
  actionLabel: {
    type: String,
    default: ''
  }
})

defineEmits(['action'])
</script>