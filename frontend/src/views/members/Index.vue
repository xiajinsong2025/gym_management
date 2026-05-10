<template>
  <div class="page-card">
    <div class="page-header">
      <div class="page-title">会员管理</div>
      <el-button type="primary" @click="openCreate">新增会员</el-button>
    </div>
    <div class="search-bar">
      <el-form :inline="true">
        <el-form-item><el-input v-model="keyword" placeholder="姓名/手机号" /></el-form-item>
        <el-form-item><el-select v-model="status" clearable placeholder="状态" style="width: 160px"><el-option v-for="s in statusItems" :key="s" :label="s" :value="s" /></el-select></el-form-item>
        <el-form-item><el-button type="primary" @click="load">查询</el-button></el-form-item>
      </el-form>
    </div>
    <div class="table-wrap">
      <el-table :data="rows" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="name" label="姓名" />
        <el-table-column prop="mobile" label="手机号" />
        <el-table-column prop="status" label="状态" width="120">
          <template #default="scope"><el-tag>{{ scope.row.status }}</el-tag></template>
        </el-table-column>
        <el-table-column label="操作" width="120">
          <template #default="scope"><el-button link type="primary" @click="openEdit(scope.row)">编辑</el-button></template>
        </el-table-column>
      </el-table>
    </div>
  </div>

  <el-dialog v-model="dialog" :title="editId ? '编辑会员' : '新增会员'" width="560" class="form-dialog">
    <el-form :model="form" label-position="top" class="form-grid">
      <el-form-item label="姓名"><el-input v-model="form.name" /></el-form-item>
      <el-form-item label="手机号"><el-input v-model="form.mobile" /></el-form-item>
      <el-form-item label="性别"><el-select v-model="form.gender"><el-option v-for="g in genderItems" :key="g" :label="g" :value="g" /></el-select></el-form-item>
      <el-form-item label="状态"><el-select v-model="form.status"><el-option v-for="s in statusItems" :key="s" :label="s" :value="s" /></el-select></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialog = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="save">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { reactive, ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { memberApi } from '@/api/members'
import type { Member, MemberCreate, MemberStatus } from '@/types'

const rows = ref<Member[]>([])
const loading = ref(false)
const saving = ref(false)
const dialog = ref(false)
const keyword = ref('')
const status = ref<string>()
const editId = ref<number>()
const statusItems: MemberStatus[] = ['normal', 'frozen', 'expired', 'lost', 'lead']
const genderItems = ['unknown', 'male', 'female']
const form = reactive<MemberCreate & { status?: MemberStatus }>({ name: '', mobile: '', gender: 'unknown', status: 'normal' })

function openCreate() {
  editId.value = undefined
  Object.assign(form, { name: '', mobile: '', gender: 'unknown', status: 'normal' })
  dialog.value = true
}
function openEdit(row: Member) {
  editId.value = row.id
  Object.assign(form, row)
  dialog.value = true
}
async function load() {
  loading.value = true
  try {
    const res = await memberApi.list({ keyword: keyword.value || undefined, status: status.value || undefined })
    rows.value = res.data.items
  } finally {
    loading.value = false
  }
}
async function save() {
  saving.value = true
  try {
    if (editId.value) await memberApi.update(editId.value, form)
    else await memberApi.create(form)
    ElMessage.success('保存成功')
    dialog.value = false
    await load()
  } finally {
    saving.value = false
  }
}
onMounted(load)
</script>
