import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useDispatchStore = defineStore('dispatch', () => {
    const dispatches = ref([])
    const pendingDispatches = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const totalDispatches = computed(() => dispatches.value.length)
    const pendingCount = computed(() => pendingDispatches.value.length)
    const activeDispatches = computed(() =>
        dispatches.value.filter(d => d.status === 'in_progress')
    )

    // Actions
    async function fetchDispatches(filters = {}) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.get_dispatches',
                args: { filters }
            })

            dispatches.value = response.message || []
            return dispatches.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchPendingDispatches() {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.get_pending_dispatches',
                args: {}
            })

            pendingDispatches.value = response.message || []
            return pendingDispatches.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function createDispatch(dispatchData) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.create_dispatch',
                args: { dispatch_data: dispatchData }
            })

            const newDispatch = response.message
            dispatches.value.unshift(newDispatch)

            return newDispatch
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function assignDriver(dispatchId, driverId, vehicleId) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.assign_driver',
                args: {
                    dispatch_id: dispatchId,
                    driver_id: driverId,
                    vehicle_id: vehicleId
                }
            })

            // Update local state
            const index = dispatches.value.findIndex(d => d.name === dispatchId)
            if (index !== -1) {
                dispatches.value[index].driver = driverId
                dispatches.value[index].vehicle = vehicleId
                dispatches.value[index].status = 'assigned'
            }

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function updateDispatchStatus(dispatchId, status) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.update_dispatch_status',
                args: {
                    dispatch_id: dispatchId,
                    status: status
                }
            })

            // Update local state
            const index = dispatches.value.findIndex(d => d.name === dispatchId)
            if (index !== -1) {
                dispatches.value[index].status = status
            }

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
        dispatches,
        pendingDispatches,
        loading,
        error,

        // Computed
        totalDispatches,
        pendingCount,
        activeDispatches,

        // Actions
        fetchDispatches,
        fetchPendingDispatches,
        createDispatch,
        assignDriver,
        updateDispatchStatus,
        clearError
    }
})
