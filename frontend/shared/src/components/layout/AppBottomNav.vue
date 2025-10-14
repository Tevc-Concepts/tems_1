<template>
  <nav class="fixed bottom-0 left-0 right-0 z-50 bg-charcoal border-t border-charcoal-light shadow-xl lg:hidden">
    <div class="max-w-screen-xl mx-auto">
      <div class="flex justify-around items-center h-16">
        <button
          v-for="item in items"
          :key="item.name"
          @click="handleNavigate(item)"
          :class="[
            'flex flex-col items-center justify-center w-full h-full space-y-1 transition-colors relative',
            isActive(item) ? 'text-neon-green' : 'text-gray-400'
          ]"
        >
          <!-- Icon -->
          <component 
            v-if="item.icon" 
            :is="item.icon" 
            :class="[
              'w-6 h-6',
              isActive(item) ? 'scale-110' : 'scale-100',
              'transition-transform'
            ]"
          />
          <svg v-else class="w-6 h-6" fill="currentColor" viewBox="0 0 20 20">
            <circle cx="10" cy="10" r="3"/>
          </svg>

          <!-- Label -->
          <span 
            :class="[
              'text-xs font-medium',
              isActive(item) ? 'font-semibold' : 'font-normal'
            ]"
          >
            {{ item.name }}
          </span>

          <!-- Badge -->
          <span
            v-if="item.badge"
            :class="[
              'absolute top-2 right-1/4 min-w-[18px] h-[18px] flex items-center justify-center px-1 text-[10px] font-bold rounded-full',
              item.badgeClass || 'bg-red-500 text-white'
            ]"
          >
            {{ formatBadge(item.badge) }}
          </span>

          <!-- Active Indicator -->
          <div
            v-if="isActive(item)"
            class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-12 h-1 bg-neon-green rounded-t-full"
          ></div>
        </button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    required: true,
    validator: (items) => {
      return items.every(item => item.name && (item.href || item.action))
    }
  },
  currentRoute: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['navigate'])

// Methods
function handleNavigate(item) {
  emit('navigate', item)
}

function isActive(item) {
  if (!item.href) return false
  return props.currentRoute === item.href || props.currentRoute.startsWith(item.href)
}

function formatBadge(badge) {
  if (typeof badge === 'number' && badge > 99) {
    return '99+'
  }
  return badge
}
</script>

<style scoped>
/* Add safe area padding for devices with notches */
nav {
  padding-bottom: env(safe-area-inset-bottom);
}
</style>
