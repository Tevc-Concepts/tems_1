import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useFleetStore = defineStore('fleet', () => {
    const vehicles = ref([])
    const activeVehicles = ref([])
    const loading = ref(false)
    const error = ref(null)
    const lastUpdate = ref(null)

    // Computed
    const totalVehicles = computed(() => vehicles.value.length)
    const activeCount = computed(() => activeVehicles.value.filter(v => v.status === 'active').length)
    const availableCount = computed(() => vehicles.value.filter(v => v.availability === 'available').length)

    // Actions
    async function fetchVehicles() {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.get_fleet_vehicles',
                args: {}
            })

            vehicles.value = response.message || []
            lastUpdate.value = new Date()
            return vehicles.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchActiveVehicles() {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.get_active_vehicles',
                args: {}
            })

            activeVehicles.value = response.message || []
            return activeVehicles.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function getVehicleLocation(vehicleId) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.get_vehicle_location',
                args: { vehicle_id: vehicleId }
            })

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function updateVehicleStatus(vehicleId, status) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.operations.update_vehicle_status',
                args: {
                    vehicle_id: vehicleId,
                    status: status
                }
            })

            // Update local state
            const index = vehicles.value.findIndex(v => v.name === vehicleId)
            if (index !== -1) {
                vehicles.value[index].status = status
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
        vehicles,
        activeVehicles,
        loading,
        error,
        lastUpdate,

        // Computed
        totalVehicles,
        activeCount,
        availableCount,

        // Actions
        fetchVehicles,
        fetchActiveVehicles,
        getVehicleLocation,
        updateVehicleStatus,
        clearError
    }
})
