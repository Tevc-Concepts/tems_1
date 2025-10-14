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
                path: 'incidents',
                name: 'Incidents',
                component: () => import('../views/Incidents.vue')
            },
            {
                path: 'incidents/:id',
                name: 'IncidentDetails',
                component: () => import('../views/IncidentDetails.vue')
            },
            {
                path: 'audits',
                name: 'SafetyAudits',
                component: () => import('../views/SafetyAudits.vue')
            },
            {
                path: 'compliance',
                name: 'Compliance',
                component: () => import('../views/Compliance.vue')
            },
            {
                path: 'risk-assessment',
                name: 'RiskAssessment',
                component: () => import('../views/RiskAssessment.vue')
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
    history: createWebHistory('/assets/tems/frontend/safety-pwa/dist/'),
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
