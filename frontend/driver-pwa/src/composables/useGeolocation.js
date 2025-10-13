import { ref, onMounted, onUnmounted } from 'vue'

export function useGeolocation(options = {}) {
    const coords = ref(null)
    const error = ref(null)
    const loading = ref(false)
    const watchId = ref(null)

    const defaultOptions = {
        enableHighAccuracy: true,
        timeout: 10000,
        maximumAge: 0,
        ...options
    }

    async function getCurrentPosition() {
        loading.value = true
        error.value = null

        return new Promise((resolve, reject) => {
            if (!navigator.geolocation) {
                const err = new Error('Geolocation is not supported by your browser')
                error.value = err
                loading.value = false
                reject(err)
                return
            }

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    coords.value = {
                        latitude: position.coords.latitude,
                        longitude: position.coords.longitude,
                        accuracy: position.coords.accuracy,
                        altitude: position.coords.altitude,
                        heading: position.coords.heading,
                        speed: position.coords.speed,
                        timestamp: position.timestamp
                    }
                    loading.value = false
                    resolve(coords.value)
                },
                (err) => {
                    error.value = err
                    loading.value = false
                    reject(err)
                },
                defaultOptions
            )
        })
    }

    function startWatching() {
        if (!navigator.geolocation) {
            error.value = new Error('Geolocation is not supported by your browser')
            return
        }

        if (watchId.value) {
            stopWatching()
        }

        watchId.value = navigator.geolocation.watchPosition(
            (position) => {
                coords.value = {
                    latitude: position.coords.latitude,
                    longitude: position.coords.longitude,
                    accuracy: position.coords.accuracy,
                    altitude: position.coords.altitude,
                    heading: position.coords.heading,
                    speed: position.coords.speed,
                    timestamp: position.timestamp
                }
                error.value = null
            },
            (err) => {
                error.value = err
            },
            defaultOptions
        )
    }

    function stopWatching() {
        if (watchId.value !== null) {
            navigator.geolocation.clearWatch(watchId.value)
            watchId.value = null
        }
    }

    onUnmounted(() => {
        stopWatching()
    })

    return {
        coords,
        error,
        loading,
        getCurrentPosition,
        startWatching,
        stopWatching
    }
}

// Calculate distance between two coordinates (Haversine formula)
export function calculateDistance(lat1, lon1, lat2, lon2) {
    const R = 6371 // Earth's radius in km
    const dLat = toRad(lat2 - lat1)
    const dLon = toRad(lon2 - lon1)

    const a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
        Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) *
        Math.sin(dLon / 2) * Math.sin(dLon / 2)

    const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a))
    const distance = R * c

    return distance // in kilometers
}

function toRad(degrees) {
    return degrees * (Math.PI / 180)
}

// Format coordinates for display
export function formatCoordinates(lat, lon) {
    const latDir = lat >= 0 ? 'N' : 'S'
    const lonDir = lon >= 0 ? 'E' : 'W'

    return `${Math.abs(lat).toFixed(6)}°${latDir}, ${Math.abs(lon).toFixed(6)}°${lonDir}`
}
