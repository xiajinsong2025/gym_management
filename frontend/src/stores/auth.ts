import { computed, ref } from 'vue'
import { defineStore } from 'pinia'

const TOKEN_KEY = 'token'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem(TOKEN_KEY))
  const permissions = ref<string[]>([])

  const isAuthenticated = computed(() => Boolean(token.value))

  function setToken(value: string | null) {
    token.value = value
    if (value) {
      localStorage.setItem(TOKEN_KEY, value)
      return
    }
    localStorage.removeItem(TOKEN_KEY)
  }

  function setPermissions(values: string[]) {
    permissions.value = values
  }

  function hasPermission(code?: string): boolean {
    if (!code) return true
    return permissions.value.includes(code)
  }

  function logout() {
    setToken(null)
    permissions.value = []
  }

  return { token, permissions, isAuthenticated, setToken, setPermissions, hasPermission, logout }
})

