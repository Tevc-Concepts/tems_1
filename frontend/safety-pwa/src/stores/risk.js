import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useRiskStore = defineStore('risk', () => {
    const riskAssessments = ref([])
    const highRisks = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const totalRisks = computed(() => riskAssessments.value.length)
    const criticalRisks = computed(() =>
        riskAssessments.value.filter(r => r.risk_level === 'critical').length
    )
    const highRiskCount = computed(() =>
        riskAssessments.value.filter(r => r.risk_level === 'high').length
    )

    // Actions
    async function fetchRiskAssessments(filters = {}) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.get_risk_assessments',
                args: { filters }
            })

            riskAssessments.value = response.message || []
            return riskAssessments.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchHighRisks() {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.get_high_risks',
                args: {}
            })

            highRisks.value = response.message || []
            return highRisks.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function createRiskAssessment(riskData) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.create_risk_assessment',
                args: { risk_data: riskData }
            })

            const newRisk = response.message
            riskAssessments.value.unshift(newRisk)

            return newRisk
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function updateMitigationPlan(riskId, mitigationPlan) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.update_mitigation_plan',
                args: {
                    risk_id: riskId,
                    mitigation_plan: mitigationPlan
                }
            })

            // Update local state
            const index = riskAssessments.value.findIndex(r => r.name === riskId)
            if (index !== -1) {
                riskAssessments.value[index].mitigation_plan = mitigationPlan
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
        riskAssessments,
        highRisks,
        loading,
        error,

        // Computed
        totalRisks,
        criticalRisks,
        highRiskCount,

        // Actions
        fetchRiskAssessments,
        fetchHighRisks,
        createRiskAssessment,
        updateMitigationPlan,
        clearError
    }
})
