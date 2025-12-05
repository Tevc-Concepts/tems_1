import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@shared'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('../views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('../views/Layout.vue'),
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
  history: createWebHistory('/driver/'),
  routes
})

// Navigation guard - enforce authentication
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()

  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    next({ name: 'Login', query: { redirect: to.fullPath } })
  } else if (to.name === 'Login' && authStore.isAuthenticated) {
    next({ name: 'Dashboard' })
  } else {
    next()
  }
})

export default router