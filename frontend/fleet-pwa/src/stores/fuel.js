import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useFuelStore = defineStore('fuel', () => {
    const fuelLogs = ref([])
    const fuelStats = ref(null)
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const totalFuelConsumed = computed(() => {
        return fuelLogs.value.reduce((sum, log) => sum + (log.quantity || 0), 0)
    })

    const averageFuelEfficiency = computed(() => {
        if (!fuelStats.value) return 0
        return fuelStats.value.average_efficiency || 0
    })

    // Actions
    async function fetchFuelLogs(filters = {}) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.get_fuel_logs',
                args: { filters }
            })

            fuelLogs.value = response.message || []
            return fuelLogs.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchFuelStats(period = 'month') {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.get_fuel_stats',
                args: { period }
            })

            fuelStats.value = response.message
            return fuelStats.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function logFuelEntry(fuelData) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.log_fuel_entry',
                args: { fuel_data: fuelData }
            })

            const newLog = response.message
            fuelLogs.value.unshift(newLog)

            return newLog
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function getFuelTrends(assetId, period = 'month') {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.get_fuel_trends',
                args: {
                    asset_id: assetId,
                    period: period
                }
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
        fuelLogs,
        fuelStats,
        loading,
        error,

        // Computed
        totalFuelConsumed,
        averageFuelEfficiency,

        // Actions
        fetchFuelLogs,
        fetchFuelStats,
        logFuelEntry,
        getFuelTrends,
        clearError
    }
})
