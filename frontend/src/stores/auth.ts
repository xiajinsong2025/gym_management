import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import type { User, Permission } from '@/types'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const token = ref<string | null>(localStorage.getItem('token'))
  const permissions = ref<string[]>([])

  const isAuthenticated = computed(() => !!token.value)

  function setToken(newToken: string) {
    token.value = newToken
    localStorage.setItem('token', newToken)
  }

  function setUser(newUser: User) {
    user.value = newUser
  }

  function setPermissions(newPermissions: string[]) {
    permissions.value = newPermissions
  }

  function hasPermission(permission: string): boolean {
    return permissions.value.includes(permission)
  }

  function logout() {
    token.value = null
    user.value = null
    permissions.value = []
    localStorage.removeItem('token')
  }

  return {
    user,
    token,
    permissions,
    isAuthenticated,
    setToken,
    setUser,
    setPermissions,
    hasPermission,
    logout
  }
})