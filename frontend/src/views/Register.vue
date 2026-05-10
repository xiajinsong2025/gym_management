<template>
  <div style="height: 100%; display: grid; place-items: center; background: #f2f5fb">
    <el-card style="width: 420px">
      <template #header><div style="font-weight: 600">注册账号</div></template>
      <el-form :model="form" label-position="top">
        <el-form-item label="用户名"><el-input v-model="form.username" /></el-form-item>
        <el-form-item label="显示名"><el-input v-model="form.display_name" /></el-form-item>
        <el-form-item label="密码"><el-input v-model="form.password" show-password /></el-form-item>
      </el-form>
      <el-alert v-if="message" :title="message" :type="ok ? 'success' : 'error'" show-icon :closable="false" />
      <div style="display: flex; justify-content: space-between; margin-top: 16px">
        <el-button link @click="router.push('/login')">返回登录</el-button>
        <el-button type="primary" :loading="loading" @click="submit">注册</el-button>
      </div>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { authApi } from '@/api/auth'

const router = useRouter()
const loading = ref(false)
const ok = ref(false)
const message = ref('')
const form = reactive({ username: '', display_name: '', password: '' })

async function submit() {
  loading.value = true
  message.value = ''
  try {
    await authApi.register(form)
    ok.value = true
    message.value = '注册成功，请返回登录'
  } catch (e: any) {
    ok.value = false
    message.value = e?.message ?? e?.detail ?? '注册失败'
  } finally {
    loading.value = false
  }
}
</script>
