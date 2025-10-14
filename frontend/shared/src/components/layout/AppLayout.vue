<template>
  <div class="min-h-screen bg-light-gray">
    <!-- Header -->
    <AppHeader
      v-if="showHeader"
      :title="title"
      :subtitle="subtitle"
      :logo="logo"
      :show-user-menu="showUserMenu"
      :show-online-status="showOnlineStatus"
      :show-sync-status="showSyncStatus"
      @logout="handleLogout"
      @profile="handleProfile"
      @settings="handleSettings"
    >
      <template #center>
        <slot name="header-center"></slot>
      </template>
      <template #actions>
        <slot name="header-actions"></slot>
      </template>
      <template #menu-items>
        <slot name="menu-items"></slot>
      </template>
    </AppHeader>

    <div class="flex h-[calc(100vh-4rem)]">
      <!-- Sidebar (Desktop) -->
      <AppSidebar
        v-if="showSidebar"
        :app-name="title"
        :navigation-items="navigationItems"
        :current-route="currentRoute"
        :is-open="isSidebarOpen"
        @navigate="handleNavigate"
        @close="closeSidebar"
      >
        <template #footer>
          <slot name="sidebar-footer"></slot>
        </template>
      </AppSidebar>

      <!-- Main Content -->
      <main 
        :class="[
          'flex-1 overflow-y-auto',
          contentClass,
          showBottomNav ? 'pb-20' : '',
          showSidebar ? 'lg:ml-0' : ''
        ]"
      >
        <!-- Page Header (optional) -->
        <div v-if="pageTitle || $slots['page-header']" class="bg-white border-b border-gray-200">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <slot name="page-header">
              <div class="flex items-center justify-between">
                <div>
                  <h1 class="text-2xl font-bold text-gray-900">{{ pageTitle }}</h1>
                  <p v-if="pageSubtitle" class="mt-1 text-sm text-gray-500">{{ pageSubtitle }}</p>
                </div>
                <slot name="page-actions"></slot>
              </div>
            </slot>
          </div>
        </div>

        <!-- Content Area -->
        <div :class="containerClass">
          <slot></slot>
        </div>
      </main>
    </div>

    <!-- Bottom Navigation (Mobile) -->
    <AppBottomNav
      v-if="showBottomNav && bottomNavItems.length > 0"
      :items="bottomNavItems"
      :current-route="currentRoute"
      @navigate="handleNavigate"
    />

    <!-- Mobile Menu Toggle (if sidebar exists) -->
    <button
      v-if="showSidebar"
      @click="openSidebar"
      class="lg:hidden fixed bottom-20 right-4 z-40 w-14 h-14 bg-neon-green text-charcoal rounded-full shadow-lg flex items-center justify-center hover:scale-110 transition-transform"
    >
      <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
      </svg>
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import AppHeader from './AppHeader.vue'
import AppSidebar from './AppSidebar.vue'
import AppBottomNav from './AppBottomNav.vue'

const props = defineProps({
  title: {
    type: String,
    default: 'TEMS'
  },
  subtitle: {
    type: String,
    default: ''
  },
  logo: {
    type: String,
    default: ''
  },
  pageTitle: {
    type: String,
    default: ''
  },
  pageSubtitle: {
    type: String,
    default: ''
  },
  showHeader: {
    type: Boolean,
    default: true
  },
  showSidebar: {
    type: Boolean,
    default: true
  },
  showBottomNav: {
    type: Boolean,
    default: true
  },
  showUserMenu: {
    type: Boolean,
    default: true
  },
  showOnlineStatus: {
    type: Boolean,
    default: true
  },
  showSyncStatus: {
    type: Boolean,
    default: true
  },
  navigationItems: {
    type: Array,
    default: () => []
  },
  bottomNavItems: {
    type: Array,
    default: () => []
  },
  currentRoute: {
    type: String,
    default: ''
  },
  containerClass: {
    type: String,
    default: 'max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6'
  },
  contentClass: {
    type: String,
    default: ''
  }
})

const emit = defineEmits(['navigate', 'logout', 'profile', 'settings'])

// Local state
const isSidebarOpen = ref(false)

// Methods
function openSidebar() {
  isSidebarOpen.value = true
}

function closeSidebar() {
  isSidebarOpen.value = false
}

function handleNavigate(item) {
  emit('navigate', item)
}

function handleLogout() {
  emit('logout')
}

function handleProfile() {
  emit('profile')
}

function handleSettings() {
  emit('settings')
}
</script>

<style scoped>
/* Custom styles if needed */
</style>
