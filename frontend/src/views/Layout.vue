<template>
  <v-app>
    <v-navigation-drawer v-model="drawer" app>
      <v-list>
        <v-list-item
          prepend-avatar="https://cdn.vuetifyjs.com/images/logos/logo.svg"
          title="健身房管理系统"
          subtitle="管理后台"
        ></v-list-item>
      </v-list>

      <v-divider></v-divider>

      <v-list dense nav>
        <v-list-item
          v-for="item in menuItems"
          :key="item.title"
          :to="item.path"
          :prepend-icon="item.icon"
          :title="item.title"
          :value="item.title"
        ></v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>健身房管理系统</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon @click="handleLogout">
        <v-icon>mdi-logout</v-icon>
      </v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const drawer = ref(true)

const menuItems = [
  { title: '会员管理', icon: 'mdi-account-group', path: '/members' },
  { title: '卡务交易', icon: 'mdi-credit-card', path: '/transactions' },
  { title: '课程管理', icon: 'mdi-calendar', path: '/courses' },
  { title: '私教管理', icon: 'mdi-dumbbell', path: '/personal-training' }
]

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>
