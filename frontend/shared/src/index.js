// Shared exports
export { default as frappeClient } from './utils/frappeClient.js'
export * from './utils/helpers.js'
export * from './utils/validators.js'
export * from './utils/formatters.js'

// Composables
export { useAuth } from './composables/useAuth.js'
export { useOfflineSync } from './composables/useOfflineSync.js'
export { useGeolocation } from './composables/useGeolocation.js'
export { useCamera } from './composables/useCamera.js'
export { useNotifications } from './composables/useNotifications.js'
export { useToast } from './composables/useToast.js'

// Stores
export { useAuthStore } from './stores/auth.js'
export { useOfflineStore } from './stores/offline.js'

// Layout Components
export { default as AppHeader } from './components/layout/AppHeader.vue'
export { default as AppSidebar } from './components/layout/AppSidebar.vue'
export { default as AppBottomNav } from './components/layout/AppBottomNav.vue'
export { default as AppLayout } from './components/layout/AppLayout.vue'

// Common Components
export { default as Button } from './components/common/Button.vue'
export { default as Input } from './components/common/Input.vue'
export { default as Select } from './components/common/Select.vue'
export { default as Modal } from './components/common/Modal.vue'
export { default as Toast } from './components/common/Toast.vue'
export { default as Loading } from './components/common/Loading.vue'
export { default as Badge } from './components/common/Badge.vue'
export { default as Card } from './components/common/Card.vue'
