import { defineStore } from 'pinia'
import { ref } from 'vue'
import frappeClient from '@/utils/frappeClient'

export const useIncidentStore = defineStore('incident', () => {
    const incidents = ref([])
    const loading = ref(false)
    const error = ref(null)

    async function reportIncident(incidentData) {
        loading.value = true
        error.value = null

        try {
            const result = await frappeClient.call('tems.api.pwa.driver.report_incident', {
                data: incidentData
            })

            // Add to local list
            incidents.value.unshift({
                name: result.incident,
                ...incidentData,
                status: 'Open',
                created: new Date().toISOString()
            })

            return result
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function uploadIncidentPhoto(file, incidentName = null) {
        try {
            const uploadResult = await frappeClient.uploadFile(
                file,
                true,
                'Home/Incidents'
            )

            return uploadResult
        } catch (err) {
            error.value = err.message
            throw err
        }
    }

    async function sendSOSAlert(location, notes = '') {
        loading.value = true

        try {
            const result = await frappeClient.call('tems.api.pwa.driver.send_sos_alert', {
                location_data: location,
                notes: notes
            })

            return result
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    async function fetchIncidents() {
        loading.value = true

        try {
            const data = await frappeClient.call('tems.api.pwa.driver.get_driver_incidents')
            incidents.value = data || []
            return data
        } catch (err) {
            error.value = err.message
            throw err
        } finally {
            loading.value = false
        }
    }

    return {
        incidents,
        loading,
        error,
        reportIncident,
        uploadIncidentPhoto,
        sendSOSAlert,
        fetchIncidents
    }
})
