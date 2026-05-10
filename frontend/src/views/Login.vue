<template>
  <div style="height: 100%; display: grid; place-items: center; background: #f2f5fb">
    <el-card style="width: 420px">
      <template #header><div style="font-weight: 600">登录系统</div></template>
      <el-form :model="form" label-position="top">
        <el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" show-password /></el-form-item>
      </el-form>
      <el-alert v-if="error" :title="error" type="error" show-icon :closable="false" />
      <div style="display: flex; justify-content: space-between; margin-top: 16px">
        <el-button link @click="router.push('/register')">注册</el-button>
        <el-button type="primary" :loading="loading" @click="submit">登录</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api/auth'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()
const loading = ref(false)
const error = ref('')
const form = reactive({ username: '', password: '' })

const ALL_PERMISSIONS = [
  'members:read', 'members:write', 'transactions:read', 'transactions:write', 'courses:read', 'courses:write',
  'pt:read', 'pt:write', 'frontdesk:read', 'frontdesk:write', 'reports:read', 'marketing:read', 'marketing:write',
]

async function submit() {
  loading.value = true
  error.value = ''
  try {
    const loginRes = await authApi.login(form)
    auth.setToken(loginRes.data.access_token)
    const permRes = await authApi.grantPermissions(ALL_PERMISSIONS)
    auth.setPermissions(permRes.data)
    router.push('/')
  } catch (e: any) {
    error.value = e?.message ?? e?.detail ?? '登录失败'
  } finally {
    loading.value = false
  }
}
</script>
