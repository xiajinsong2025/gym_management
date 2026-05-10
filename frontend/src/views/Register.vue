<template>
  <v-container fluid fill-height class="login-container">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="4">
        <v-card class="elevation-12">
          <v-toolbar dark color="primary">
            <v-toolbar-title>健身房管理系统 - 注册</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" v-model="valid" @submit.prevent="handleRegister">
              <v-text-field
                v-model="form.username"
                prepend-icon="mdi-account"
                name="username"
                label="用户名 *"
                type="text"
                :rules="[rules.required, rules.minLength]"
                :error-messages="errors.username"
              ></v-text-field>
              <v-text-field
                v-model="form.display_name"
                prepend-icon="mdi-account-circle"
                name="display_name"
                label="显示名称 *"
                type="text"
                :rules="[rules.required]"
              ></v-text-field>
              <v-text-field
                v-model="form.password"
                prepend-icon="mdi-lock"
                name="password"
                label="密码 *"
                type="password"
                :rules="[rules.required, rules.passwordLength]"
                :error-messages="errors.password"
              ></v-text-field>
              <v-text-field
                v-model="form.confirmPassword"
                prepend-icon="mdi-lock-check"
                name="confirmPassword"
                label="确认密码 *"
                type="password"
                :rules="[rules.required, rules.passwordMatch]"
              ></v-text-field>
              <v-alert v-if="errorMessage" type="error" class="mt-3">
                {{ errorMessage }}
              </v-alert>
              <v-alert v-if="successMessage" type="success" class="mt-3">
                {{ successMessage }}
              </v-alert>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn text @click="goToLogin">返回登录</v-btn>
            <v-spacer></v-spacer>
            <v-btn
              color="primary"
              :loading="loading"
              :disabled="!valid"
              @click="handleRegister"
            >
              注册
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
import { authApi } from '@/api/auth'

const router = useRouter()

const form = reactive({
  username: '',
  display_name: '',
  password: '',
  confirmPassword: ''
})

const valid = ref(false)
const loading = ref(false)
const errorMessage = ref('')
const successMessage = ref('')
const formRef = ref()

const errors = reactive({
  username: '',
  password: ''
})

const rules = {
  required: (value: string) => !!value || '此字段为必填项',
  minLength: (value: string) => value.length >= 3 || '用户名至少3个字符',
  passwordLength: (value: string) => value.length >= 6 || '密码至少6个字符',
  passwordMatch: (value: string) => value === form.password || '两次密码不一致'
}

async function handleRegister() {
  if (!valid.value) return

  loading.value = true
  errorMessage.value = ''
  successMessage.value = ''

  try {
    const response = await authApi.register({
      username: form.username,
      password: form.password,
      display_name: form.display_name
    })

    if (response.code === 0) {
      successMessage.value = '注册成功！3秒后跳转到登录页面...'
      setTimeout(() => {
        router.push('/login')
      }, 3000)
    } else {
      errorMessage.value = response.message || '注册失败'
    }
  } catch (error: any) {
    errorMessage.value = error.message || '注册失败，请检查网络连接'
  } finally {
    loading.value = false
  }
}

function goToLogin() {
  router.push('/login')
}
</script>

<style scoped>
.login-container {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  min-height: 100vh;
}
</style>
