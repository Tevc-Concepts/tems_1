import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useAuditStore = defineStore('audit', () => {
    const audits = ref([])
    const upcomingAudits = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const totalAudits = computed(() => audits.value.length)
    const completedAudits = computed(() =>
        audits.value.filter(a => a.status === 'completed').length
    )
    const pendingAudits = computed(() =>
        audits.value.filter(a => a.status === 'scheduled' || a.status === 'in_progress')
    )

    // Actions
    async function fetchAudits(filters = {}) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.get_audits',
                args: { filters }
            })

            audits.value = response.message || []
            return audits.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchUpcomingAudits() {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.get_upcoming_audits',
                args: {}
            })

            upcomingAudits.value = response.message || []
            return upcomingAudits.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function scheduleAudit(auditData) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.schedule_audit',
                args: { audit_data: auditData }
            })

            const newAudit = response.message
            audits.value.unshift(newAudit)

            return newAudit
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function submitAuditFindings(auditId, findings) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.submit_audit_findings',
                args: {
                    audit_id: auditId,
                    findings: findings
                }
            })

            // Update local state
            const index = audits.value.findIndex(a => a.name === auditId)
            if (index !== -1) {
                audits.value[index].status = 'completed'
                audits.value[index].findings = findings
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
        audits,
        upcomingAudits,
        loading,
        error,

        // Computed
        totalAudits,
        completedAudits,
        pendingAudits,

        // Actions
        fetchAudits,
        fetchUpcomingAudits,
        scheduleAudit,
        submitAuditFindings,
        clearError
    }
})
