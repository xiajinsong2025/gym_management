<template>
  <div class="page-card">
    <div class="page-header">
      <div class="page-title">菜单管理</div>
      <el-button type="primary" @click="openCreate">新增菜单</el-button>
    </div>
    <div class="table-wrap">
      <el-table :data="rows" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="72" />
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="path" label="路径" />
        <el-table-column prop="permission_code" label="权限码" />
        <el-table-column prop="sort_order" label="排序" width="80" />
        <el-table-column label="可见" width="80">
          <template #default="scope"><el-tag :type="scope.row.is_visible ? 'success' : 'info'">{{ scope.row.is_visible ? '是' : '否' }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="90">
          <template #default="scope"><el-button link type="primary" @click="openEdit(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>
    </div>
  </div>

  <el-dialog v-model="dialog" :title="editId ? '编辑菜单' : '新增菜单'" width="640" class="form-dialog">
    <el-form :model="form" label-position="top" class="form-grid">
      <el-form-item label="标题"><el-input v-model="form.title" /></el-form-item>
      <el-form-item label="路径"><el-input v-model="form.path" /></el-form-item>
      <el-form-item label="父级ID"><el-input-number v-model="form.parent_id" :min="0" :controls="false" /></el-form-item>
      <el-form-item label="排序"><el-input-number v-model="form.sort_order" :min="0" /></el-form-item>
      <el-form-item label="组件"><el-input v-model="form.component" /></el-form-item>
      <el-form-item label="图标"><el-input v-model="form.icon" /></el-form-item>
      <el-form-item class="full" label="权限码"><el-input v-model="form.permission_code" /></el-form-item>
      <el-form-item label="可见"><el-switch v-model="form.is_visible" /></el-form-item>
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
import type { SystemMenu } from '@/types'

const rows = ref<SystemMenu[]>([])
const loading = ref(false)
const saving = ref(false)
const dialog = ref(false)
const editId = ref<number>()
const form = reactive({ parent_id: 0, title: '', path: '', component: '', icon: '', permission_code: '', sort_order: 0, is_visible: true })

async function load() {
  loading.value = true
  try {
    const res = await systemApi.listMenus()
    rows.value = res.data.items
  } finally {
    loading.value = false
  }
}
function openCreate() {
  editId.value = undefined
  Object.assign(form, { parent_id: 0, title: '', path: '', component: '', icon: '', permission_code: '', sort_order: 0, is_visible: true })
  dialog.value = true
}
function openEdit(row: SystemMenu) {
  editId.value = row.id
  Object.assign(form, { parent_id: row.parent_id || 0, title: row.title, path: row.path, component: row.component || '', icon: row.icon || '', permission_code: row.permission_code || '', sort_order: row.sort_order, is_visible: row.is_visible })
  dialog.value = true
}
async function save() {
  saving.value = true
  try {
    const payload = {
      parent_id: form.parent_id || null,
      title: form.title,
      path: form.path,
      component: form.component || null,
      icon: form.icon || null,
      permission_code: form.permission_code || null,
      sort_order: form.sort_order,
      is_visible: form.is_visible,
    }
    if (editId.value) await systemApi.updateMenu(editId.value, payload)
    else await systemApi.createMenu(payload)
    ElMessage.success('保存成功')
    dialog.value = false
    await load()
  } finally {
    saving.value = false
  }
}
onMounted(load)
</script>
