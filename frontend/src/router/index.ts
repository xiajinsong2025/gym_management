import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes: RouteRecordRaw[] = [
  { path: '/login', name: 'Login', component: () => import('@/views/Login.vue'), meta: { title: '登录' } },
  { path: '/register', name: 'Register', component: () => import('@/views/Register.vue'), meta: { title: '注册' } },
  { path: '/403', name: 'Forbidden', component: () => import('@/views/exception/403.vue'), meta: { title: '403' } },
  {
    path: '/',
    component: () => import('@/views/Layout.vue'),
    redirect: '/dashboard',
    children: [
      { path: 'dashboard', name: 'Dashboard', component: () => import('@/views/dashboard/Index.vue'), meta: { title: '工作台' } },
      { path: 'members', name: 'Members', component: () => import('@/views/members/Index.vue'), meta: { title: '会员管理', permission: 'members:read' } },
      { path: 'transactions', name: 'Transactions', component: () => import('@/views/transactions/Index.vue'), meta: { title: '卡务交易', permission: 'transactions:read' } },
      { path: 'courses', name: 'Courses', component: () => import('@/views/courses/Index.vue'), meta: { title: '课程管理', permission: 'courses:read' } },
      { path: 'personal-training', name: 'PersonalTraining', component: () => import('@/views/personal-training/Index.vue'), meta: { title: '私教管理', permission: 'pt:read' } },
      { path: 'front-desk', name: 'FrontDesk', component: () => import('@/views/front-desk/Index.vue'), meta: { title: '前台业务', permission: 'frontdesk:read' } },
      { path: 'reports', name: 'Reports', component: () => import('@/views/reports/Index.vue'), meta: { title: '经营报表', permission: 'reports:read' } },
      { path: 'marketing', name: 'Marketing', component: () => import('@/views/marketing/Index.vue'), meta: { title: '营销中心', permission: 'marketing:read' } },
      { path: 'system/users', name: 'SystemUsers', component: () => import('@/views/system/users/Index.vue'), meta: { title: '用户管理' } },
      { path: 'system/roles', name: 'SystemRoles', component: () => import('@/views/system/roles/Index.vue'), meta: { title: '角色管理' } },
      { path: 'system/menus', name: 'SystemMenus', component: () => import('@/views/system/menus/Index.vue'), meta: { title: '菜单管理' } },
      { path: 'system/departments', name: 'SystemDepartments', component: () => import('@/views/system/departments/Index.vue'), meta: { title: '部门管理' } },
      { path: 'system/logs', name: 'SystemLogs', component: () => import('@/views/system/logs/Index.vue'), meta: { title: '操作日志' } },
    ],
  },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: () => import('@/views/exception/404.vue'), meta: { title: '404' } },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

function firstAllowedPath(auth: ReturnType<typeof useAuthStore>) {
  const list: Array<[string, string]> = [
    ['/dashboard', ''],
    ['/members', 'members:read'],
    ['/transactions', 'transactions:read'],
    ['/courses', 'courses:read'],
    ['/personal-training', 'pt:read'],
    ['/front-desk', 'frontdesk:read'],
    ['/reports', 'reports:read'],
    ['/marketing', 'marketing:read'],
  ]
  return list.find((item) => auth.hasPermission(item[1]))?.[0] ?? '/dashboard'
}

router.beforeEach((to) => {
  const auth = useAuthStore()
  const publicPaths = new Set(['/login', '/register', '/403'])

  if (!publicPaths.has(to.path) && !auth.isAuthenticated) return '/login'
  if (auth.isAuthenticated && (to.path === '/login' || to.path === '/register')) return firstAllowedPath(auth)

  const required = to.meta.permission as string | undefined
  if (required && !auth.hasPermission(required)) return '/403'
  return true
})

export default router
