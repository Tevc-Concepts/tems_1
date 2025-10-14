import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { frappeClient } from '@shared'

export const useIncidentStore = defineStore('incident', () => {
    const incidents = ref([])
    const criticalIncidents = ref([])
    const loading = ref(false)
    const error = ref(null)

    // Computed
    const totalIncidents = computed(() => incidents.value.length)
    const criticalCount = computed(() =>
        incidents.value.filter(i => i.severity === 'critical').length
    )
    const openIncidents = computed(() =>
        incidents.value.filter(i => i.status === 'open' || i.status === 'investigating')
    )

    // Actions
    async function fetchIncidents(filters = {}) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.get_incidents',
                args: { filters }
            })

            incidents.value = response.message || []
            return incidents.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchCriticalIncidents() {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.get_critical_incidents',
                args: {}
            })

            criticalIncidents.value = response.message || []
            return criticalIncidents.value
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function reportIncident(incidentData) {
        loading.value = true
        error.value = null

        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.report_incident',
                args: { incident_data: incidentData }
            })

            const newIncident = response.message
            incidents.value.unshift(newIncident)

            return newIncident
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function updateIncidentStatus(incidentId, status, notes = '') {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.update_incident_status',
                args: {
                    incident_id: incidentId,
                    status: status,
                    notes: notes
                }
            })

            // Update local state
            const index = incidents.value.findIndex(i => i.name === incidentId)
            if (index !== -1) {
                incidents.value[index].status = status
            }

            return response.message
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function assignInvestigator(incidentId, investigatorId) {
        try {
            const response = await frappeClient.call({
                method: 'tems.api.pwa.safety.assign_investigator',
                args: {
                    incident_id: incidentId,
                    investigator_id: investigatorId
                }
            })

            // Update local state
            const index = incidents.value.findIndex(i => i.name === incidentId)
            if (index !== -1) {
                incidents.value[index].investigator = investigatorId
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
        incidents,
        criticalIncidents,
        loading,
        error,

        // Computed
        totalIncidents,
        criticalCount,
        openIncidents,

        // Actions
        fetchIncidents,
        fetchCriticalIncidents,
        reportIncident,
        updateIncidentStatus,
        assignInvestigator,
        clearError
    }
})
