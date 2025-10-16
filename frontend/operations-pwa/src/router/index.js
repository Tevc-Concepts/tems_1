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
                component: () => import('../views/Dashboard.vue')
            },
            {
                path: 'fleet',
                name: 'FleetTracking',
                component: () => import('../views/FleetTracking.vue')
            },
            {
                path: 'fleet/:vehicleId',
                name: 'VehicleDetails',
                component: () => import('../views/VehicleDetails.vue')
            },
            {
                path: 'dispatch',
                name: 'DispatchManagement',
                component: () => import('../views/DispatchManagement.vue')
            },
            {
                path: 'routes',
                name: 'RouteManagement',
                component: () => import('../views/RouteManagement.vue')
            },
            {
                path: 'analytics',
                name: 'Analytics',
                component: () => import('../views/Analytics.vue')
            },
            {
                path: 'settings',
                name: 'Settings',
                component: () => import('../views/Settings.vue')
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory('/operations/'),
    routes
})

// Navigation guard
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
