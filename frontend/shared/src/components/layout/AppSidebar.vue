<template>
  <aside
    :class="[
      'fixed inset-y-0 left-0 z-40 w-64 bg-charcoal shadow-xl transform transition-transform duration-300 ease-in-out',
      isOpen ? 'translate-x-0' : '-translate-x-full',
      'lg:translate-x-0 lg:static lg:z-0'
    ]"
  >
    <!-- Sidebar Header -->
    <div class="h-16 flex items-center justify-between px-4 border-b border-charcoal-light">
      <div class="flex items-center space-x-3">
        <div class="h-10 w-10 bg-neon-green rounded-lg flex items-center justify-center">
          <span class="text-charcoal font-bold text-xl">{{ appInitial }}</span>
        </div>
        <span class="text-white font-semibold">{{ appName }}</span>
      </div>
      <button
        @click="closeSidebar"
        class="lg:hidden text-gray-400 hover:text-white"
      >
        <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
        </svg>
      </button>
    </div>

    <!-- Navigation -->
    <nav class="flex-1 overflow-y-auto px-3 py-4 space-y-1">
      <template v-for="item in navigationItems" :key="item.name">
        <!-- Regular Menu Item -->
        <a
          v-if="!item.children"
          :href="item.href"
          @click.prevent="handleNavigate(item)"
          :class="[
            'flex items-center space-x-3 px-3 py-2.5 rounded-lg transition-colors',
            isActive(item) 
              ? 'bg-neon-green text-charcoal' 
              : 'text-gray-300 hover:bg-charcoal-light hover:text-white'
          ]"
        >
          <component v-if="item.icon" :is="item.icon" class="w-5 h-5" />
          <svg v-else class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <circle cx="10" cy="10" r="3"/>
          </svg>
          <span class="font-medium">{{ item.name }}</span>
          <span
            v-if="item.badge"
            :class="[
              'ml-auto px-2 py-0.5 text-xs rounded-full',
              item.badgeClass || 'bg-neon-green text-charcoal'
            ]"
          >
            {{ item.badge }}
          </span>
        </a>

        <!-- Menu Item with Children -->
        <div v-else>
          <button
            @click="toggleSubmenu(item.name)"
            :class="[
              'w-full flex items-center justify-between px-3 py-2.5 rounded-lg transition-colors',
              isSubmenuOpen(item.name) || hasActiveChild(item)
                ? 'bg-charcoal-light text-white'
                : 'text-gray-300 hover:bg-charcoal-light hover:text-white'
            ]"
          >
            <div class="flex items-center space-x-3">
              <component v-if="item.icon" :is="item.icon" class="w-5 h-5" />
              <span class="font-medium">{{ item.name }}</span>
            </div>
            <svg
              class="w-4 h-4 transition-transform"
              :class="{ 'rotate-180': isSubmenuOpen(item.name) }"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path fill-rule="evenodd" d="M5.293 7.293a1 1 0 011.414 0L10 10.586l3.293-3.293a1 1 0 111.414 1.414l-4 4a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414z" clip-rule="evenodd"/>
            </svg>
          </button>

          <!-- Submenu -->
          <transition
            enter-active-class="transition ease-out duration-100"
            enter-from-class="transform opacity-0 -translate-y-2"
            enter-to-class="transform opacity-100 translate-y-0"
            leave-active-class="transition ease-in duration-75"
            leave-from-class="transform opacity-100 translate-y-0"
            leave-to-class="transform opacity-0 -translate-y-2"
          >
            <div v-if="isSubmenuOpen(item.name)" class="ml-8 mt-1 space-y-1">
              <a
                v-for="child in item.children"
                :key="child.name"
                :href="child.href"
                @click.prevent="handleNavigate(child)"
                :class="[
                  'block px-3 py-2 rounded-lg transition-colors text-sm',
                  isActive(child)
                    ? 'bg-neon-green text-charcoal'
                    : 'text-gray-400 hover:bg-charcoal-light hover:text-white'
                ]"
              >
                {{ child.name }}
              </a>
            </div>
          </transition>
        </div>
      </template>
    </nav>

    <!-- Sidebar Footer -->
    <div class="border-t border-charcoal-light p-4">
      <slot name="footer">
        <div class="text-xs text-gray-500 text-center">
          TEMS © {{ currentYear }}
        </div>
      </slot>
    </div>
  </aside>

  <!-- Overlay for mobile -->
  <div
    v-if="isOpen"
    @click="closeSidebar"
    class="fixed inset-0 bg-black bg-opacity-50 z-30 lg:hidden"
  ></div>
</template>

<script setup>
import { ref, computed } from 'vue'

const props = defineProps({
  appName: {
    type: String,
    default: 'TEMS'
  },
  navigationItems: {
    type: Array,
    required: true
  },
  currentRoute: {
    type: String,
    default: ''
  },
  isOpen: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['navigate', 'close'])

// Local state
const openSubmenus = ref(new Set())

// Computed
const appInitial = computed(() => {
  return props.appName.charAt(0).toUpperCase()
})

const currentYear = computed(() => {
  return new Date().getFullYear()
})

// Methods
function handleNavigate(item) {
  emit('navigate', item)
  if (window.innerWidth < 1024) {
    closeSidebar()
  }
}

function closeSidebar() {
  emit('close')
}

function toggleSubmenu(name) {
  if (openSubmenus.value.has(name)) {
    openSubmenus.value.delete(name)
  } else {
    openSubmenus.value.add(name)
  }
}

function isSubmenuOpen(name) {
  return openSubmenus.value.has(name)
}

function isActive(item) {
  if (!item.href) return false
  return props.currentRoute === item.href || props.currentRoute.startsWith(item.href)
}

function hasActiveChild(item) {
  if (!item.children) return false
  return item.children.some(child => isActive(child))
}
</script>

<style scoped>
/* Custom scrollbar for navigation */
nav::-webkit-scrollbar {
  width: 6px;
}

nav::-webkit-scrollbar-track {
  background: rgba(0, 0, 0, 0.1);
}

nav::-webkit-scrollbar-thumb {
  background: rgba(57, 255, 20, 0.3);
  border-radius: 3px;
}

nav::-webkit-scrollbar-thumb:hover {
  background: rgba(57, 255, 20, 0.5);
}
</style>
