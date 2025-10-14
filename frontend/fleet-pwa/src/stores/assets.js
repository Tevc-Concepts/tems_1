import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useAssetStore = defineStore('asset', () => {
    const assets = ref([])
    const categories = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const totalAssets = computed(() => assets.value.length)
    const activeAssets = computed(() =>
        assets.value.filter(a => a.status === 'active').length
    )
    const underMaintenanceCount = computed(() =>
        assets.value.filter(a => a.status === 'under_maintenance').length
    )
    const assetUtilization = computed(() => {
        if (totalAssets.value === 0) return 0
        return ((activeAssets.value / totalAssets.value) * 100).toFixed(1)
    })

    // Actions
    async function fetchAssets(filters = {}) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.get_assets',
                args: { filters }
            })

            assets.value = response.message || []
            return assets.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function getAssetDetails(assetId) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.get_asset_details',
                args: { asset_id: assetId }
            })

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function updateAssetStatus(assetId, status, notes = '') {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.update_asset_status',
                args: {
                    asset_id: assetId,
                    status: status,
                    notes: notes
                }
            })

            // Update local state
            const index = assets.value.findIndex(a => a.name === assetId)
            if (index !== -1) {
                assets.value[index].status = status
            }

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function fetchCategories() {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.fleet.get_asset_categories',
                args: {}
            })

            categories.value = response.message || []
            return categories.value
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
        assets,
        categories,
        loading,
        error,

        // Computed
        totalAssets,
        activeAssets,
        underMaintenanceCount,
        assetUtilization,

        // Actions
        fetchAssets,
        getAssetDetails,
        updateAssetStatus,
        fetchCategories,
        clearError
    }
})
