import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import frappeClient from '../utils/frappeClient.js'

/**
 * Authentication store
 * Manages user authentication state and employee profile
 */
export const useAuthStore = defineStore('auth', () => {
    const user = ref(null)
    const employee = ref(null)
    const permissions = ref([])
    const roles = ref([])
    const loading = ref(false)
    const error = ref(null)

    const isAuthenticated = computed(() => !!user.value)
    const userName = computed(() => employee.value?.employee_name || user.value?.full_name || 'User')
    const userInitials = computed(() => {
        const name = userName.value
        return name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase()
    })

    /**
     * Fetch current user information and employee details
     */
    async function fetchUserInfo() {
        loading.value = true
        error.value = null

        try {
            // Get logged user
            const currentUser = await frappeClient.getCurrentUser()

            if (!currentUser || currentUser === 'Guest') {
                throw new Error('Not authenticated')
            }

            // Get user doc
            const userData = await frappeClient.getDoc('User', currentUser)
            user.value = userData
            roles.value = userData.roles?.map(r => r.role) || []

            // Get employee details if linked
            if (userData.name) {
                try {
                    const employeeList = await frappeClient.getList(
                        'Employee',
                        ['name', 'employee_name', 'designation', 'image', 'department', 'cell_number'],
                        [['user_id', '=', userData.name]],
                        1
                    )

                    if (employeeList && employeeList.length > 0) {
                        employee.value = employeeList[0]
                    }
                } catch (err) {
                    console.warn('Employee not found for user:', err)
                }
            }

            return userData
        } catch (err) {
            error.value = err.message
            console.error('Failed to fetch user info:', err)
            throw err
        } finally {
            loading.value = false
        }
    }

    /**
     * Check if user has a specific role
     */
    function hasRole(role) {
        return roles.value.includes(role)
    }

    /**
     * Check if user has any of the specified roles
     */
    function hasAnyRole(roleList) {
        return roleList.some(role => roles.value.includes(role))
    }

    /**
     * Check if user has permission for a doctype action
     */
    function hasPermission(doctype, action = 'read') {
        // TODO: Implement proper permission check via Frappe API
        return true
    }

    /**
     * Logout current user
     */
    async function logout() {
        try {
            await frappeClient.call('logout')
            user.value = null
            employee.value = null
            permissions.value = []
            roles.value = []

            // Redirect to login
            window.location.href = '/login'
        } catch (err) {
            console.error('Logout failed:', err)
            error.value = err.message
        }
    }

    /**
     * Clear auth state
     */
    function clearAuth() {
        user.value = null
        employee.value = null
        permissions.value = []
        roles.value = []
        error.value = null
    }

    return {
        user,
        employee,
        permissions,
        roles,
        loading,
        error,
        isAuthenticated,
        userName,
        userInitials,
        fetchUserInfo,
        hasRole,
        hasAnyRole,
        hasPermission,
        logout,
        clearAuth
    }
})
