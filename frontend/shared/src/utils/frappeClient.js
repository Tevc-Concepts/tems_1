import localforage from 'localforage'

/**
 * Enhanced Frappe API Client with offline-first capabilities
 * Supports session-based and JWT authentication
 * Implements request queuing and automatic sync
 */
class FrappeClient {
    constructor() {
        this.baseURL = window.location.origin
        this.isOnline = navigator.onLine
        this.retryAttempts = 3
        this.retryDelay = 1000 // ms

        // Setup offline storage
        this.offlineStore = localforage.createInstance({
            name: 'tems_offline'
        })

        this.queueStore = localforage.createInstance({
            name: 'tems_queue'
        })

        // Monitor online status
        window.addEventListener('online', () => {
            this.isOnline = true
            this.syncOfflineData()
        })

        window.addEventListener('offline', () => {
            this.isOnline = false
        })
    }

    /**
     * Call a Frappe RPC method
     * @param {string} method - Method path (e.g., 'tems.api.pwa.driver.get_trips')
     * @param {object} args - Method arguments
     * @param {boolean} cache - Whether to cache the result
     * @returns {Promise<any>}
     */
    async call(method, args = {}, cache = false) {
        const endpoint = `${this.baseURL}/api/method/${method}`
        const cacheKey = `rpc:${method}:${JSON.stringify(args)}`

        try {
            const response = await this.fetchWithRetry(endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Frappe-CSRF-Token': this.getCSRFToken(),
                },
                credentials: 'include',
                body: JSON.stringify(args),
            })

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}))
                throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
            }

            const data = await response.json()

            // Cache if requested
            if (cache && data.message) {
                await this.offlineStore.setItem(cacheKey, {
                    data: data.message,
                    timestamp: Date.now()
                })
            }

            return data.message
        } catch (error) {
            if (!this.isOnline) {
                return this.handleOfflineRequest(cacheKey)
            }
            throw error
        }
    }

    /**
     * Get a single document
     * @param {string} doctype - DocType name
     * @param {string} name - Document name
     * @returns {Promise<object>}
     */
    async getDoc(doctype, name) {
        const endpoint = `${this.baseURL}/api/resource/${doctype}/${name}`
        const cacheKey = `${doctype}:${name}`

        try {
            const response = await this.fetchWithRetry(endpoint, {
                credentials: 'include',
                headers: {
                    'X-Frappe-CSRF-Token': this.getCSRFToken(),
                }
            })

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

            const data = await response.json()

            // Cache for offline use
            await this.offlineStore.setItem(cacheKey, {
                data: data.data,
                timestamp: Date.now()
            })

            return data.data
        } catch (error) {
            if (!this.isOnline) {
                const cached = await this.offlineStore.getItem(cacheKey)
                if (cached) return cached.data
            }
            throw error
        }
    }

    /**
     * Get a list of documents
     * @param {string} doctype - DocType name
     * @param {string[]} fields - Fields to fetch
     * @param {object|array} filters - Frappe filters
     * @param {number} limit - Number of records
     * @param {string} orderBy - Order by clause
     * @returns {Promise<array>}
     */
    async getList(doctype, fields = ['name'], filters = {}, limit = 20, orderBy = 'modified desc') {
        const endpoint = `${this.baseURL}/api/resource/${doctype}`
        const params = new URLSearchParams({
            fields: JSON.stringify(fields),
            filters: JSON.stringify(filters),
            limit_page_length: limit,
            order_by: orderBy
        })

        const cacheKey = `list:${doctype}:${JSON.stringify(filters)}:${limit}`

        try {
            const response = await this.fetchWithRetry(`${endpoint}?${params}`, {
                credentials: 'include',
                headers: {
                    'X-Frappe-CSRF-Token': this.getCSRFToken(),
                }
            })

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

            const data = await response.json()

            // Cache list for offline
            await this.offlineStore.setItem(cacheKey, {
                data: data.data,
                timestamp: Date.now()
            })

            return data.data
        } catch (error) {
            if (!this.isOnline) {
                const cached = await this.offlineStore.getItem(cacheKey)
                if (cached) return cached.data
            }
            throw error
        }
    }

    /**
     * Update a document
     * @param {string} doctype - DocType name
     * @param {string} name - Document name
     * @param {object} data - Fields to update
     * @returns {Promise<object>}
     */
    async setDoc(doctype, name, data) {
        if (!this.isOnline) {
            return this.queueOfflineWrite(doctype, name, data, 'update')
        }

        const endpoint = `${this.baseURL}/api/resource/${doctype}/${name}`

        const response = await this.fetchWithRetry(endpoint, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'X-Frappe-CSRF-Token': this.getCSRFToken(),
            },
            credentials: 'include',
            body: JSON.stringify(data),
        })

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)

        const result = await response.json()

        // Update cache
        await this.offlineStore.setItem(`${doctype}:${name}`, {
            data: result.data,
            timestamp: Date.now()
        })

        return result.data
    }

    /**
     * Create a new document
     * @param {string} doctype - DocType name
     * @param {object} data - Document data
     * @returns {Promise<object>}
     */
    async createDoc(doctype, data) {
        if (!this.isOnline) {
            return this.queueOfflineWrite(doctype, null, data, 'create')
        }

        const endpoint = `${this.baseURL}/api/resource/${doctype}`

        const response = await this.fetchWithRetry(endpoint, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Frappe-CSRF-Token': this.getCSRFToken(),
            },
            credentials: 'include',
            body: JSON.stringify(data),
        })

        if (!response.ok) {
            const errorData = await response.json().catch(() => ({}))
            throw new Error(errorData.message || 'Failed to create document')
        }

        return await response.json()
    }

    /**
     * Delete a document
     * @param {string} doctype - DocType name
     * @param {string} name - Document name
     * @returns {Promise<void>}
     */
    async deleteDoc(doctype, name) {
        if (!this.isOnline) {
            return this.queueOfflineWrite(doctype, name, {}, 'delete')
        }

        const endpoint = `${this.baseURL}/api/resource/${doctype}/${name}`

        const response = await fetch(endpoint, {
            method: 'DELETE',
            headers: {
                'X-Frappe-CSRF-Token': this.getCSRFToken(),
            },
            credentials: 'include',
        })

        if (!response.ok) throw new Error('Failed to delete document')

        // Remove from cache
        await this.offlineStore.removeItem(`${doctype}:${name}`)
    }

    /**
     * Upload a file to Frappe
     * @param {File} file - File object
     * @param {boolean} isPrivate - Whether file is private
     * @param {string} folder - Folder path
     * @param {string} doctype - Optional: Link to doctype
     * @param {string} docname - Optional: Link to document
     * @returns {Promise<object>}
     */
    async uploadFile(file, isPrivate = false, folder = 'Home', doctype = null, docname = null) {
        const formData = new FormData()
        formData.append('file', file)
        formData.append('is_private', isPrivate ? 1 : 0)
        formData.append('folder', folder)

        if (doctype) formData.append('doctype', doctype)
        if (docname) formData.append('docname', docname)

        const response = await fetch(`${this.baseURL}/api/method/upload_file`, {
            method: 'POST',
            headers: {
                'X-Frappe-CSRF-Token': this.getCSRFToken(),
            },
            credentials: 'include',
            body: formData
        })

        if (!response.ok) throw new Error('Upload failed')

        const data = await response.json()
        return data.message
    }

    /**
     * Fetch with automatic retry on failure
     * @private
     */
    async fetchWithRetry(url, options, attempt = 1) {
        try {
            return await fetch(url, options)
        } catch (error) {
            if (attempt < this.retryAttempts && this.isOnline) {
                await this.delay(this.retryDelay * attempt)
                return this.fetchWithRetry(url, options, attempt + 1)
            }
            throw error
        }
    }

    /**
     * Get CSRF token from meta tag or cookie
     * @private
     */
    getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') ||
            document.cookie.split('; ').find(row => row.startsWith('csrf_token='))?.split('=')[1] || ''
    }

    /**
     * Queue a write operation for offline sync
     * @private
     */
    async queueOfflineWrite(doctype, name, data, action = 'update') {
        const queue = await this.queueStore.getItem('write_queue') || []
        const queueItem = {
            id: `${Date.now()}_${Math.random()}`,
            doctype,
            name,
            data,
            action,
            timestamp: Date.now()
        }

        queue.push(queueItem)
        await this.queueStore.setItem('write_queue', queue)

        return {
            queued: true,
            offline: true,
            queueId: queueItem.id,
            message: 'Saved offline. Will sync when online.'
        }
    }

    /**
     * Sync all queued offline operations
     * @returns {Promise<object>} Sync results
     */
    async syncOfflineData() {
        const queue = await this.queueStore.getItem('write_queue') || []
        if (queue.length === 0) return { synced: 0, failed: [] }

        const results = {
            synced: 0,
            failed: []
        }

        for (const item of queue) {
            try {
                if (item.action === 'create') {
                    await this.createDoc(item.doctype, item.data)
                } else if (item.action === 'update') {
                    await this.setDoc(item.doctype, item.name, item.data)
                } else if (item.action === 'delete') {
                    await this.deleteDoc(item.doctype, item.name)
                }
                results.synced++
            } catch (error) {
                console.error('Sync failed for item:', item, error)
                results.failed.push({ item, error: error.message })
            }
        }

        // Remove synced items
        if (results.failed.length === 0) {
            await this.queueStore.setItem('write_queue', [])
        } else {
            await this.queueStore.setItem('write_queue', results.failed.map(f => f.item))
        }

        return results
    }

    /**
     * Get count of pending offline operations
     * @returns {Promise<number>}
     */
    async getPendingQueueCount() {
        const queue = await this.queueStore.getItem('write_queue') || []
        return queue.length
    }

    /**
     * Handle offline request by returning cached data
     * @private
     */
    async handleOfflineRequest(cacheKey) {
        const cached = await this.offlineStore.getItem(cacheKey)

        if (cached) return cached.data

        return {
            offline: true,
            error: 'No cached data available',
            message: 'You are offline and this data is not cached'
        }
    }

    /**
     * Clear all cached data and queue
     * @returns {Promise<void>}
     */
    async clearCache() {
        await this.offlineStore.clear()
        await this.queueStore.clear()
    }

    /**
     * Simple delay utility
     * @private
     */
    delay(ms) {
        return new Promise(resolve => setTimeout(resolve, ms))
    }

    /**
     * Check authentication status
     * @returns {Promise<boolean>}
     */
    async isAuthenticated() {
        try {
            const response = await fetch(`${this.baseURL}/api/method/frappe.auth.get_logged_user`, {
                credentials: 'include',
                headers: {
                    'X-Frappe-CSRF-Token': this.getCSRFToken(),
                }
            })

            if (!response.ok) return false

            const data = await response.json()
            return data.message && data.message !== 'Guest'
        } catch {
            return false
        }
    }

    /**
     * Get current logged-in user
     * @returns {Promise<string|null>}
     */
    async getCurrentUser() {
        try {
            const response = await fetch(`${this.baseURL}/api/method/frappe.auth.get_logged_user`, {
                credentials: 'include',
                headers: {
                    'X-Frappe-CSRF-Token': this.getCSRFToken(),
                }
            })

            if (!response.ok) return null

            const data = await response.json()
            return data.message !== 'Guest' ? data.message : null
        } catch {
            return null
        }
    }
}

export const frappeClient = new FrappeClient()
export default frappeClient
