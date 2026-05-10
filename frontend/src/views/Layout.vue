<template>
  <div class="app-shell">
    <aside class="app-side">
      <div class="brand">
        <div class="brand-mark">GYM</div>
        <div class="brand-text">
          <div class="brand-title">运营中台</div>
          <div class="brand-sub">Multi Fitness Console</div>
        </div>
      </div>
      <el-scrollbar class="menu-scroll">
        <el-menu :default-active="$route.path" background-color="#0f172a" text-color="#94a3b8" active-text-color="#ffffff" router>
          <template v-for="group in menuGroups" :key="group.title">
            <el-sub-menu :index="group.title">
              <template #title>
                <el-icon><component :is="group.icon" /></el-icon>
                <span>{{ group.title }}</span>
              </template>
              <el-menu-item v-for="item in group.items" :key="item.path" :index="item.path">
                {{ item.title }}
              </el-menu-item>
            </el-sub-menu>
          </template>
        </el-menu>
      </el-scrollbar>
    </aside>

    <section class="app-main">
      <header class="top-bar">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item>控制台</el-breadcrumb-item>
          <el-breadcrumb-item>{{ String($route.meta.title || '') }}</el-breadcrumb-item>
        </el-breadcrumb>
        <div class="top-actions">
          <el-dropdown>
            <span class="user-trigger">
              <el-avatar :size="28">A</el-avatar>
              <span>Admin</span>
            </span>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item @click="toDashboard">工作台</el-dropdown-item>
                <el-dropdown-item divided @click="logout">退出登录</el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </header>

      <div class="tabs-bar">
        <el-tag
          v-for="tab in worktabs"
          :key="tab.path"
          :type="tab.path === $route.path ? 'primary' : 'info'"
          effect="plain"
          class="tab-pill"
          @click="router.push(tab.path)"
        >
          {{ tab.title }}
        </el-tag>
      </div>

      <main class="content-wrap">
        <router-view />
      </main>
    </section>
  </div>
</template>

<script setup lang="ts">
import { computed, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { DataLine, Monitor, Setting } from '@element-plus/icons-vue'

type MenuItem = { title: string; path: string; permission?: string }
type MenuGroup = { title: string; icon: unknown; items: MenuItem[] }

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const menuGroups = computed<MenuGroup[]>(() => [
  {
    title: '运营看板',
    icon: DataLine,
    items: [{ title: '工作台', path: '/dashboard' }, { title: '经营报表', path: '/reports', permission: 'reports:read' }],
  },
  {
    title: '业务管理',
    icon: Monitor,
    items: [
      { title: '会员管理', path: '/members', permission: 'members:read' },
      { title: '卡务交易', path: '/transactions', permission: 'transactions:read' },
      { title: '课程管理', path: '/courses', permission: 'courses:read' },
      { title: '私教管理', path: '/personal-training', permission: 'pt:read' },
      { title: '前台业务', path: '/front-desk', permission: 'frontdesk:read' },
      { title: '营销中心', path: '/marketing', permission: 'marketing:read' },
    ].filter((item) => auth.hasPermission(item.permission)),
  },
  {
    title: '系统管理',
    icon: Setting,
    items: [
      { title: '用户管理', path: '/system/users' },
      { title: '角色管理', path: '/system/roles' },
      { title: '菜单管理', path: '/system/menus' },
      { title: '部门管理', path: '/system/departments' },
      { title: '操作日志', path: '/system/logs' },
    ],
  },
])

const worktabs = computed(() => {
  const current = { path: route.path, title: String(route.meta.title || route.path) }
  const all = menuGroups.value.flatMap((group) => group.items.map((m) => ({ path: m.path, title: m.title })))
  return Array.from(new Map([current, ...all].map((x) => [x.path, x])).values()).slice(0, 10)
})

watch(
  () => route.path,
  () => {
    document.title = `${String(route.meta.title || 'Admin')} - Gym`
  },
  { immediate: true }
)

function toDashboard() {
  router.push('/dashboard')
}

function logout() {
  auth.logout()
  router.push('/login')
}
</script>
