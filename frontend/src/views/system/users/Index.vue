<template>
  <div class="page-card">
    <div class="page-header">
      <div class="page-title">用户管理</div>
      <el-button type="primary" @click="openCreate">新增用户</el-button>
    </div>
    <div class="search-bar">
      <el-form :inline="true">
        <el-form-item><el-input v-model="keyword" placeholder="用户名/姓名" /></el-form-item>
        <el-form-item><el-button type="primary" @click="load">查询</el-button></el-form-item>
      </el-form>
    </div>
    <div class="table-wrap">
      <el-table :data="rows" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="72" />
        <el-table-column prop="username" label="用户名" />
        <el-table-column prop="display_name" label="姓名" />
        <el-table-column prop="mobile" label="手机号" />
        <el-table-column prop="is_active" label="状态" width="100">
          <template #default="scope"><el-tag :type="scope.row.is_active ? 'success' : 'danger'">{{ scope.row.is_active ? '启用' : '停用' }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="90">
          <template #default="scope"><el-button link type="primary" @click="openEdit(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>
    </div>
  </div>

  <el-dialog v-model="dialog" :title="editId ? '编辑用户' : '新增用户'" width="560" class="form-dialog">
    <el-form :model="form" label-position="top" class="form-grid">
      <el-form-item label="用户名"><el-input v-model="form.username" :disabled="Boolean(editId)" /></el-form-item>
      <el-form-item label="姓名"><el-input v-model="form.display_name" /></el-form-item>
      <el-form-item label="手机号"><el-input v-model="form.mobile" /></el-form-item>
      <el-form-item label="邮箱"><el-input v-model="form.email" /></el-form-item>
      <el-form-item v-if="!editId" label="密码"><el-input v-model="form.password" show-password /></el-form-item>
      <el-form-item label="状态"><el-switch v-model="form.is_active" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialog = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="save">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { systemApi } from '@/api/system'
import type { SystemUser } from '@/types'

const rows = ref<SystemUser[]>([])
const loading = ref(false)
const saving = ref(false)
const dialog = ref(false)
const editId = ref<number>()
const keyword = ref('')
const form = reactive({
  username: '',
  password: '',
  display_name: '',
  mobile: '',
  email: '',
  is_active: true,
  is_superuser: false,
})

async function load() {
  loading.value = true
  try {
    const res = await systemApi.listUsers({ keyword: keyword.value || undefined })
    rows.value = res.data.items
  } finally {
    loading.value = false
  }
}
function openCreate() {
  editId.value = undefined
  Object.assign(form, { username: '', password: '', display_name: '', mobile: '', email: '', is_active: true, is_superuser: false })
  dialog.value = true
}
function openEdit(row: SystemUser) {
  editId.value = row.id
  Object.assign(form, { username: row.username, password: '', display_name: row.display_name, mobile: row.mobile || '', email: row.email || '', is_active: row.is_active, is_superuser: row.is_superuser })
  dialog.value = true
}
async function save() {
  saving.value = true
  try {
    if (editId.value) {
      await systemApi.updateUser(editId.value, { display_name: form.display_name, mobile: form.mobile || null, email: form.email || null, is_active: form.is_active, is_superuser: form.is_superuser })
    } else {
      await systemApi.createUser({ username: form.username, password: form.password, display_name: form.display_name, mobile: form.mobile || null, email: form.email || null, is_active: form.is_active, is_superuser: form.is_superuser })
    }
    ElMessage.success('保存成功')
    dialog.value = false
    await load()
  } finally {
    saving.value = false
  }
}
onMounted(load)
</script>
