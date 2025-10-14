import { useAuthStore } from '../stores/auth.js'
import { storeToRefs } from 'pinia'

/**
 * Authentication composable
 * Provides reactive access to authentication state and methods
 * 
 * @example
 * ```javascript
 * import { useAuth } from '@shared/composables/useAuth'
 * 
 * const { user, isAuthenticated, logout } = useAuth()
 * ```
 */
export function useAuth() {
    const authStore = useAuthStore()

    // Convert store state to refs for reactivity
    const {
        user,
        employee,
        isAuthenticated,
        userName,
        userInitials,
        roles,
        loading,
        error
    } = storeToRefs(authStore)

    return {
        // State
        user,
        employee,
        isAuthenticated,
        userName,
        userInitials,
        roles,
        loading,
        error,

        // Actions
        fetchUserInfo: authStore.fetchUserInfo,
        hasRole: authStore.hasRole,
        hasAnyRole: authStore.hasAnyRole,
        hasPermission: authStore.hasPermission,
        logout: authStore.logout,
        clearAuth: authStore.clearAuth
    }
}
