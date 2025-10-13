import localforage from 'localforage'

class FrappeClient {
  constructor() {
    this.baseURL = window.location.origin
    this.isOnline = navigator.onLine
    
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

  async call(method, args = {}) {
    const endpoint = `${this.baseURL}/api/method/${method}`
    
    try {
      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-Frappe-CSRF-Token': this.getCSRFToken(),
        },
        credentials: 'include',
        body: JSON.stringify(args),
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || `HTTP error! status: ${response.status}`)
      }

      const data = await response.json()
      return data.message
    } catch (error) {
      if (!this.isOnline) {
        return this.handleOfflineRequest(method, args)
      }
      throw error
    }
  }

  async getDoc(doctype, name) {
    const endpoint = `${this.baseURL}/api/resource/${doctype}/${name}`
    const cacheKey = `${doctype}:${name}`
    
    try {
      const response = await fetch(endpoint, {
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

  async getList(doctype, fields = ['name'], filters = {}, limit = 20, orderBy = 'modified desc') {
    const endpoint = `${this.baseURL}/api/resource/${doctype}`
    const params = new URLSearchParams({
      fields: JSON.stringify(fields),
      filters: JSON.stringify(filters),
      limit_page_length: limit,
      order_by: orderBy
    })

    const cacheKey = `list:${doctype}:${JSON.stringify(filters)}`

    try {
      const response = await fetch(`${endpoint}?${params}`, {
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

  async setDoc(doctype, name, data) {
    if (!this.isOnline) {
      return this.queueOfflineWrite(doctype, name, data, 'update')
    }

    const endpoint = `${this.baseURL}/api/resource/${doctype}/${name}`
    
    const response = await fetch(endpoint, {
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

  async createDoc(doctype, data) {
    if (!this.isOnline) {
      return this.queueOfflineWrite(doctype, null, data, 'create')
    }

    const endpoint = `${this.baseURL}/api/resource/${doctype}`
    
    const response = await fetch(endpoint, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-Frappe-CSRF-Token': this.getCSRFToken(),
      },
      credentials: 'include',
      body: JSON.stringify(data),
    })

    if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`)
    
    return await response.json()
  }

  async uploadFile(file, isPrivate = false, folder = 'Home') {
    const formData = new FormData()
    formData.append('file', file)
    formData.append('is_private', isPrivate ? 1 : 0)
    formData.append('folder', folder)

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

  getCSRFToken() {
    return document.querySelector('meta[name="csrf-token"]')?.getAttribute('content') || 
           document.cookie.split('; ').find(row => row.startsWith('csrf_token='))?.split('=')[1] || ''
  }

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

  async syncOfflineData() {
    const queue = await this.queueStore.getItem('write_queue') || []
    if (queue.length === 0) return { synced: 0 }
    
    const results = {
      synced: 0,
      failed: []
    }
    
    for (const item of queue) {
      try {
        if (item.action === 'create') {
          await this.createDoc(item.doctype, item.data)
        } else {
          await this.setDoc(item.doctype, item.name, item.data)
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

  async getPendingQueueCount() {
    const queue = await this.queueStore.getItem('write_queue') || []
    return queue.length
  }

  async handleOfflineRequest(method, args) {
    const cacheKey = `rpc:${method}:${JSON.stringify(args)}`
    const cached = await this.offlineStore.getItem(cacheKey)
    
    if (cached) return cached.data
    
    return { 
      offline: true, 
      error: 'No cached data available',
      message: 'You are offline and this data is not cached' 
    }
  }

  async clearCache() {
    await this.offlineStore.clear()
    await this.queueStore.clear()
  }
}

export const frappeClient = new FrappeClient()
export default frappeClient