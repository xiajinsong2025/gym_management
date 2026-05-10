<template>
  <div class="app-shell">
    <aside class="app-side">
      <div style="padding: 16px 14px; border-bottom: 1px solid #1f2937">
        <div style="font-size: 16px; font-weight: 700; color: #fff">Gym Admin</div>
        <div style="font-size: 12px; color: #93a2b8; margin-top: 4px">FastAPI + Vue</div>
      </div>
      <el-menu :default-active="$route.path" background-color="#111827" text-color="#cbd5e1" active-text-color="#fff" router>
        <el-menu-item v-for="item in menus" :key="item.path" :index="item.path">
          <el-icon><component :is="item.icon" /></el-icon>
          <span>{{ item.title }}</span>
        </el-menu-item>
      </el-menu>
    </aside>

    <section class="app-main">
      <header class="top-bar">
        <el-breadcrumb separator="/">
          <el-breadcrumb-item>首页</el-breadcrumb-item>
          <el-breadcrumb-item>{{ String($route.meta.title || '') }}</el-breadcrumb-item>
        </el-breadcrumb>
        <div>
          <el-button type="primary" plain size="small">工作台</el-button>
          <el-button size="small" @click="logout">退出</el-button>
        </div>
      </header>

      <div style="padding: 0 16px 8px; background: #fff; border-bottom: 1px solid var(--border-color)">
        <el-tag
          v-for="tab in worktabs"
          :key="tab.path"
          :type="tab.path === $route.path ? 'primary' : 'info'"
          effect="plain"
          style="margin: 8px 8px 0 0; cursor: pointer"
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
import { User, CreditCard, Calendar, DataAnalysis, Promotion, Briefcase, Van } from '@element-plus/icons-vue'

const router = useRouter()
const route = useRoute()
const auth = useAuthStore()

const allMenus = [
  { title: '会员管理', path: '/members', permission: 'members:read', icon: User },
  { title: '卡务交易', path: '/transactions', permission: 'transactions:read', icon: CreditCard },
  { title: '课程管理', path: '/courses', permission: 'courses:read', icon: Calendar },
  { title: '私教管理', path: '/personal-training', permission: 'pt:read', icon: Briefcase },
  { title: '前台业务', path: '/front-desk', permission: 'frontdesk:read', icon: Van },
  { title: '经营报表', path: '/reports', permission: 'reports:read', icon: DataAnalysis },
  { title: '营销中心', path: '/marketing', permission: 'marketing:read', icon: Promotion },
]

const menus = computed(() => allMenus.filter((m) => auth.hasPermission(m.permission)))
const worktabs = computed(() => {
  const current = { path: route.path, title: String(route.meta.title || route.path) }
  const base = menus.value.map((m) => ({ path: m.path, title: m.title }))
  return Array.from(new Map([current, ...base].map((x) => [x.path, x])).values()).slice(0, 8)
})

watch(
  () => route.path,
  () => {
    document.title = `${String(route.meta.title || 'Admin')} - Gym`
  },
  { immediate: true }
)

function logout() {
  auth.logout()
  router.push('/login')
}
</script>
