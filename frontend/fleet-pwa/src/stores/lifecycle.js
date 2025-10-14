import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useLifecycleStore = defineStore('lifecycle', () => {
    const lifecycleData = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const totalAssets = computed(() => lifecycleData.value.length)
    const nearingEndOfLife = computed(() =>
        lifecycleData.value.filter(a => a.remaining_life_percent < 20).length
    )

    // Actions
    async function fetchLifecycleData(filters = {}) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.get_lifecycle_data',
                args: { filters }
            })

            lifecycleData.value = response.message || []
            return lifecycleData.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function getAssetLifecycle(assetId) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.get_asset_lifecycle',
                args: { asset_id: assetId }
            })

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function calculateDepreciation(assetId) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.calculate_depreciation',
                args: { asset_id: assetId }
            })

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function updateLifecycleMilestone(assetId, milestone, status) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.update_lifecycle_milestone',
                args: {
                    asset_id: assetId,
                    milestone: milestone,
                    status: status
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
        lifecycleData,
        loading,
        error,

        // Computed
        totalAssets,
        nearingEndOfLife,

        // Actions
        fetchLifecycleData,
        getAssetLifecycle,
        calculateDepreciation,
        updateLifecycleMilestone,
        clearError
    }
})
