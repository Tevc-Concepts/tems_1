import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import frappeClient from '@/utils/frappeClient'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const employee = ref(null)
  const loading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!user.value)
  const driverName = computed(() => employee.value?.employee_name || user.value?.full_name || 'Driver')

  async function fetchUserInfo() {
    loading.value = true
    error.value = null
    
    try {
      const userData = await frappeClient.call('frappe.auth.get_logged_user')
      user.value = userData
      
      // Get employee details
      const employeeData = await frappeClient.call('frappe.client.get_value', {
        doctype: 'Employee',
        filters: { user_id: userData.name },
        fieldname: ['name', 'employee_name', 'designation', 'image']
      })
      
      employee.value = employeeData
      
      return userData
    } catch (err) {
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function logout() {
    try {
      await frappeClient.call('logout')
      user.value = null
      employee.value = null
      window.location.href = '/login'
    } catch (err) {
      console.error('Logout failed:', err)
    }
  }

  return {
    user,
    employee,
    loading,
    error,
    isAuthenticated,
    driverName,
    fetchUserInfo,
    logout
  }
})