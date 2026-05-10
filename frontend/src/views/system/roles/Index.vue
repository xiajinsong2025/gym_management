<template>
  <div class="page-card">
    <div class="page-header">
      <div class="page-title">角色管理</div>
      <el-button type="primary" @click="openCreate">新增角色</el-button>
    </div>
    <div class="table-wrap">
      <el-table :data="rows" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="72" />
        <el-table-column prop="name" label="角色名" />
        <el-table-column prop="code" label="角色编码" />
        <el-table-column prop="description" label="描述" />
        <el-table-column label="状态" width="100">
          <template #default="scope"><el-tag :type="scope.row.is_active ? 'success' : 'danger'">{{ scope.row.is_active ? '启用' : '停用' }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="150">
          <template #default="scope">
            <el-button link type="primary" @click="openEdit(scope.row)">编辑</el-button>
            <el-button link @click="openPermission(scope.row)">权限</el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>

  <el-dialog v-model="dialog" :title="editId ? '编辑角色' : '新增角色'" width="520" class="form-dialog">
    <el-form :model="form" label-position="top" class="form-grid">
      <el-form-item label="角色名"><el-input v-model="form.name" /></el-form-item>
      <el-form-item label="角色编码"><el-input v-model="form.code" :disabled="Boolean(editId)" /></el-form-item>
      <el-form-item class="full" label="描述"><el-input v-model="form.description" /></el-form-item>
      <el-form-item label="状态"><el-switch v-model="form.is_active" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialog = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="save">保存</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="permissionDialog" title="角色权限配置" width="640" class="form-dialog">
    <el-form label-position="top">
      <el-form-item label="权限码">
        <el-checkbox-group v-model="permissionForm.codes">
          <el-checkbox v-for="item in permissionOptions" :key="item.code" :label="item.code">
            {{ item.code }}
          </el-checkbox>
        </el-checkbox-group>
      </el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="permissionDialog = false">取消</el-button>
      <el-button type="primary" :loading="permissionSaving" @click="savePermissions">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { systemApi } from '@/api/system'
import type { PermissionItem, SystemRole } from '@/types'

const rows = ref<SystemRole[]>([])
const loading = ref(false)
const saving = ref(false)
const permissionSaving = ref(false)
const dialog = ref(false)
const permissionDialog = ref(false)
const editId = ref<number>()
const permissionRoleId = ref<number>()
const form = reactive({ name: '', code: '', description: '', is_active: true })
const permissionForm = reactive<{ codes: string[] }>({ codes: [] })
const permissionOptions = ref<PermissionItem[]>([])

async function load() {
  loading.value = true
  try {
    const res = await systemApi.listRoles()
    rows.value = res.data.items
  } finally {
    loading.value = false
  }
}
function openCreate() {
  editId.value = undefined
  Object.assign(form, { name: '', code: '', description: '', is_active: true })
  dialog.value = true
}
function openEdit(row: SystemRole) {
  editId.value = row.id
  Object.assign(form, { name: row.name, code: row.code, description: row.description || '', is_active: row.is_active })
  dialog.value = true
}
async function save() {
  saving.value = true
  try {
    if (editId.value) await systemApi.updateRole(editId.value, { name: form.name, description: form.description || null, is_active: form.is_active })
    else await systemApi.createRole({ name: form.name, code: form.code, description: form.description || null, is_active: form.is_active })
    ElMessage.success('保存成功')
    dialog.value = false
    await load()
  } finally {
    saving.value = false
  }
}
async function openPermission(row: SystemRole) {
  permissionRoleId.value = row.id
  permissionDialog.value = true
  const [all, selected] = await Promise.all([systemApi.listPermissions(), systemApi.getRolePermissions(row.id)])
  permissionOptions.value = all.data
  permissionForm.codes = [...selected.data]
}
async function savePermissions() {
  if (!permissionRoleId.value) return
  permissionSaving.value = true
  try {
    await systemApi.updateRolePermissions(permissionRoleId.value, permissionForm.codes)
    ElMessage.success('权限已更新')
    permissionDialog.value = false
  } finally {
    permissionSaving.value = false
  }
}
onMounted(load)
</script>
