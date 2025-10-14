import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useComplianceStore = defineStore('compliance', () => {
    const complianceItems = ref([])
    const expiringItems = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const totalItems = computed(() => complianceItems.value.length)
    const compliantCount = computed(() =>
        complianceItems.value.filter(i => i.status === 'compliant').length
    )
    const nonCompliantCount = computed(() =>
        complianceItems.value.filter(i => i.status === 'non_compliant').length
    )
    const complianceRate = computed(() => {
        if (totalItems.value === 0) return 0
        return ((compliantCount.value / totalItems.value) * 100).toFixed(1)
    })

    // Actions
    async function fetchComplianceItems(filters = {}) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.get_compliance_items',
                args: { filters }
            })

            complianceItems.value = response.message || []
            return complianceItems.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchExpiringItems(days = 30) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.get_expiring_compliance',
                args: { days }
            })

            expiringItems.value = response.message || []
            return expiringItems.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function updateComplianceStatus(itemId, status, notes = '') {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.update_compliance_status',
                args: {
                    item_id: itemId,
                    status: status,
                    notes: notes
                }
            })

            // Update local state
            const index = complianceItems.value.findIndex(i => i.name === itemId)
            if (index !== -1) {
                complianceItems.value[index].status = status
            }

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function renewCompliance(itemId, expiryDate) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.renew_compliance',
                args: {
                    item_id: itemId,
                    expiry_date: expiryDate
                }
            })

            // Update local state
            const index = complianceItems.value.findIndex(i => i.name === itemId)
            if (index !== -1) {
                complianceItems.value[index].expiry_date = expiryDate
                complianceItems.value[index].status = 'compliant'
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
        complianceItems,
        expiringItems,
        loading,
        error,

        // Computed
        totalItems,
        compliantCount,
        nonCompliantCount,
        complianceRate,

        // Actions
        fetchComplianceItems,
        fetchExpiringItems,
        updateComplianceStatus,
        renewCompliance,
        clearError
    }
})
