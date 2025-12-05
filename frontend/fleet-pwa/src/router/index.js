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
                redirect: '/dashboard'
            },
            {
                path: 'dashboard',
                name: 'Dashboard',
                component: () => import('../views/Dashboard.vue')
            },
            {
                path: 'assets',
                name: 'AssetManagement',
                component: () => import('../views/AssetManagement.vue')
            },
            {
                path: 'assets/:id',
                name: 'AssetDetails',
                component: () => import('../views/AssetDetails.vue')
            },
            {
                path: 'maintenance',
                name: 'MaintenanceSchedule',
                component: () => import('../views/MaintenanceSchedule.vue')
            },
            {
                path: 'fuel',
                name: 'FuelAnalytics',
                component: () => import('../views/FuelAnalytics.vue')
            },
            {
                path: 'lifecycle',
                name: 'LifecycleTracking',
                component: () => import('../views/LifecycleTracking.vue')
            },
            {
                path: 'reports',
                name: 'Reports',
                component: () => import('../views/Reports.vue')
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
    history: createWebHistory('/fleet/'),
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
