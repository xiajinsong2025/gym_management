import { createRouter, createWebHistory } from 'vue-router'
import type { RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/register',
    name: 'Register',
    component: () => import('@/views/Register.vue'),
    meta: { requiresAuth: false }
  },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    meta: { requiresAuth: true },
    children: [
      {
        path: '',
        redirect: '/members'
      },
      {
        path: 'members',
        name: 'Members',
        component: () => import('@/views/members/Index.vue'),
        meta: { permission: 'members:read' }
      },
      {
        path: 'transactions',
        name: 'Transactions',
        component: () => import('@/views/transactions/Index.vue'),
        meta: { permission: 'transactions:read' }
      },
      {
        path: 'courses',
        name: 'Courses',
        component: () => import('@/views/courses/Index.vue'),
        meta: { permission: 'courses:read' }
      },
      {
        path: 'personal-training',
        name: 'PersonalTraining',
        component: () => import('@/views/personal-training/Index.vue'),
        meta: { permission: 'pt:read' }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

router.beforeEach((to, from, next) => {
  const token = localStorage.getItem('token')

  if (to.meta.requiresAuth && !token) {
    next('/login')
  } else if (to.path === '/login' && token) {
    next('/')
  } else {
    next()
  }
})

export default router
