<template>
  <div class="page-card">
    <div class="page-header">
      <div class="page-title">部门管理</div>
      <el-button type="primary" @click="openCreate">新增部门</el-button>
    </div>
    <div class="table-wrap">
      <el-table :data="rows" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="72" />
        <el-table-column prop="name" label="部门名称" />
        <el-table-column prop="parent_id" label="父级ID" width="90" />
        <el-table-column prop="sort_order" label="排序" width="80" />
        <el-table-column label="状态" width="100">
          <template #default="scope"><el-tag :type="scope.row.is_active ? 'success' : 'danger'">{{ scope.row.is_active ? '启用' : '停用' }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="90">
          <template #default="scope"><el-button link type="primary" @click="openEdit(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>
    </div>
  </div>

  <el-dialog v-model="dialog" :title="editId ? '编辑部门' : '新增部门'" width="520" class="form-dialog">
    <el-form :model="form" label-position="top" class="form-grid">
      <el-form-item label="部门名称"><el-input v-model="form.name" /></el-form-item>
      <el-form-item label="父级ID"><el-input-number v-model="form.parent_id" :min="0" :controls="false" /></el-form-item>
      <el-form-item label="排序"><el-input-number v-model="form.sort_order" :min="0" /></el-form-item>
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
import type { SystemDepartment } from '@/types'

const rows = ref<SystemDepartment[]>([])
const loading = ref(false)
const saving = ref(false)
const dialog = ref(false)
const editId = ref<number>()
const form = reactive({ name: '', parent_id: 0, sort_order: 0, is_active: true })

async function load() {
  loading.value = true
  try {
    const res = await systemApi.listDepartments()
    rows.value = res.data.items
  } finally {
    loading.value = false
  }
}
function openCreate() {
  editId.value = undefined
  Object.assign(form, { name: '', parent_id: 0, sort_order: 0, is_active: true })
  dialog.value = true
}
function openEdit(row: SystemDepartment) {
  editId.value = row.id
  Object.assign(form, { name: row.name, parent_id: row.parent_id || 0, sort_order: row.sort_order, is_active: row.is_active })
  dialog.value = true
}
async function save() {
  saving.value = true
  try {
    const payload = { name: form.name, parent_id: form.parent_id || null, sort_order: form.sort_order, is_active: form.is_active }
    if (editId.value) await systemApi.updateDepartment(editId.value, payload)
    else await systemApi.createDepartment(payload)
    ElMessage.success('保存成功')
    dialog.value = false
    await load()
  } finally {
    saving.value = false
  }
}
onMounted(load)
</script>
