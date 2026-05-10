<template>
  <v-container fluid fill-height class="login-container">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>健身房管理系统</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="handleLogin">
              <v-text-field
                v-model="form.username"
                prepend-icon="mdi-account"
                name="username"
                label="用户名"
                type="text"
                :rules="[rules.required]"
                :error-messages="errors.username"
              ></v-text-field>
              <v-text-field
                v-model="form.password"
                prepend-icon="mdi-lock"
                name="password"
                label="密码"
                type="password"
                :rules="[rules.required]"
                :error-messages="errors.password"
              ></v-text-field>
              <v-alert v-if="errorMessage" type="error" class="mt-3">
                {{ errorMessage }}
              </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="goToRegister">注册账号</v-btn>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="!valid"
              @click="handleLogin"
            >
              登录
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authApi } from '@/api/auth'

const router = useRouter()
const authStore = useAuthStore()

const form = reactive({
  username: '',
  password: ''
})

const valid = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const errors = reactive({
  username: '',
  password: ''
})

const rules = {
  required: (value: string) => !!value || '此字段为必填项'
}

function goToRegister() {
  router.push('/register')
}

async function handleLogin() {
  if (!valid.value) return

  loading.value = true
  errorMessage.value = ''

  try {
    const response = await authApi.login({
      username: form.username,
      password: form.password
    })

    if (response.code === 0 && response.data) {
      authStore.setToken(response.data.access_token)

      // Grant permissions for development
      await authApi.grantPermissions([
        'members:read',
        'members:write',
        'transactions:read',
        'transactions:write',
        'courses:read',
        'courses:write',
        'pt:read',
        'pt:write',
        'frontdesk:read',
        'frontdesk:write',
        'reports:read',
        'marketing:read',
        'marketing:write'
      ])

      authStore.setPermissions([
        'members:read',
        'members:write',
        'transactions:read',
        'transactions:write',
        'courses:read',
        'courses:write',
        'pt:read',
        'pt:write',
        'frontdesk:read',
        'frontdesk:write',
        'reports:read',
        'marketing:read',
        'marketing:write'
      ])

      router.push('/')
    } else {
      errorMessage.value = response.message || '登录失败'
    }
  } catch (error: any) {
    errorMessage.value = error.message || '登录失败，请检查网络连接'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}
</style>
