import { createRouter, createWebHistory } from 'vue-router'
import { useAuth as useAuthStore } from '@shared'

const routes = [
  {
    path: '/driver/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/driver',
    component: () => import('../components/layout/AppLayout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        name: 'Dashboard',
        component: () => import('../views/Dashboard.vue'),
        meta: { title: 'Dashboard', icon: 'Home' }
      },
      {
        path: 'trips',
        name: 'TripManagement',
        component: () => import('../views/TripManagement.vue'),
        meta: { title: 'My Trips', icon: 'Route' }
      },
      {
        path: 'trips/:id',
        name: 'TripDetails',
        component: () => import('../views/TripDetails.vue'),
        meta: { title: 'Trip Details' }
      },
      {
        path: 'trips/:id/cargo',
        name: 'CargoManagement',
        component: () => import('../views/CargoManagement.vue'),
        meta: { title: 'Cargo Management' }
      },
      {
        path: 'trips/:id/passengers',
        name: 'PassengerManagement',
        component: () => import('../views/PassengerManagement.vue'),
        meta: { title: 'Passenger Management' }
      },
      {
        path: 'inspection',
        name: 'VehicleInspection',
        component: () => import('../views/VehicleInspection.vue'),
        meta: { title: 'Vehicle Inspection', icon: 'Clipboard' }
      },
      {
        path: 'incident',
        name: 'IncidentReport',
        component: () => import('../views/IncidentReport.vue'),
        meta: { title: 'Report Incident', icon: 'AlertTriangle' }
      },
      {
        path: 'fuel',
        name: 'FuelLog',
        component: () => import('../views/FuelLog.vue'),
        meta: { title: 'Log Fuel', icon: 'Fuel' }
      },
      {
        path: 'messages',
        name: 'Communication',
        component: () => import('../views/Communication.vue'),
        meta: { title: 'Messages', icon: 'MessageCircle' }
      },
      {
        path: 'notifications',
        name: 'Notifications',
        component: () => import('../views/Notifications.vue'),
        meta: { title: 'Notifications', icon: 'Bell' }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: () => import('../views/Profile.vue'),
        meta: { title: 'My Profile', icon: 'User' }
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('../views/Settings.vue'),
        meta: { title: 'Settings', icon: 'Settings' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth) {
    // If not authenticated, try to fetch user info first
    if (!authStore.isAuthenticated) {
      try {
        await authStore.fetchUserInfo()

        // Check again after fetch - if still not authenticated, redirect to login
        if (!authStore.isAuthenticated) {
          console.warn('User not authenticated, redirecting to login')
          next({ name: 'Login', query: { redirect: to.fullPath } })
          return
        }

        // User is authenticated, proceed
        next()
      } catch (error) {
        console.error('Authentication check failed:', error)
        next({ name: 'Login', query: { redirect: to.fullPath } })
        return
      }
    } else {
      // Already authenticated, proceed
      next()
    }
  } else if (to.name === 'Login' && authStore.isAuthenticated) {
    // Already logged in, redirect to dashboard
    next('/driver')
  } else {
    // Route doesn't require auth, proceed
    next()
  }
})

export default router