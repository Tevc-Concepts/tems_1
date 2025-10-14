import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useRouteStore = defineStore('route', () => {
    const routes = ref([])
    const activeRoutes = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const totalRoutes = computed(() => routes.value.length)
    const activeCount = computed(() => activeRoutes.value.length)

    // Actions
    async function fetchRoutes() {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.get_routes',
                args: {}
            })

            routes.value = response.message || []
            return routes.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchActiveRoutes() {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.get_active_routes',
                args: {}
            })

            activeRoutes.value = response.message || []
            return activeRoutes.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function getRouteDetails(routeId) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.get_route_details',
                args: { route_id: routeId }
            })

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function optimizeRoute(routeId) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.optimize_route',
                args: { route_id: routeId }
            })

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    function clearError() {
        error.value = null
    }

    return {
        // State
        routes,
        activeRoutes,
        loading,
        error,

        // Computed
        totalRoutes,
        activeCount,

        // Actions
        fetchRoutes,
        fetchActiveRoutes,
        getRouteDetails,
        optimizeRoute,
        clearError
    }
})
