<template>
  <div class="page-card">
    <div class="page-header">
      <div class="page-title">私教管理</div>
      <el-button type="primary" @click="dialog = true">新增课包</el-button>
    </div>
    <div class="table-wrap">
      <el-tabs v-model="tab">
        <el-tab-pane label="课包" name="packages">
          <el-table :data="packages" border v-loading="loading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="member_id" label="会员ID" />
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="total_sessions" label="总课时" />
            <el-table-column prop="remaining_sessions" label="剩余课时" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="排课" name="sessions">
          <el-table :data="sessions" border v-loading="loading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="package_id" label="课包ID" />
            <el-table-column prop="member_id" label="会员ID" />
            <el-table-column prop="start_time" label="开始时间" />
            <el-table-column prop="status" label="状态" />
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>

  <el-dialog v-model="dialog" title="新增私教课包" width="520">
    <el-form :model="newPkg" label-position="top">
      <el-form-item label="会员ID"><el-input-number v-model="newPkg.member_id" :min="1" style="width: 100%" /></el-form-item>
      <el-form-item label="名称"><el-input v-model="newPkg.name" /></el-form-item>
      <el-form-item label="总课时"><el-input-number v-model="newPkg.total_sessions" :min="1" style="width: 100%" /></el-form-item>
      <el-form-item label="剩余课时"><el-input-number v-model="newPkg.remaining_sessions" :min="0" style="width: 100%" /></el-form-item>
      <el-form-item label="金额(分)"><el-input-number v-model="newPkg.amount_cents" :min="0" style="width: 100%" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialog = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="createPackage">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { ptApi } from '@/api/business'
import type { PtPackage, PtSession } from '@/types'

const tab = ref('packages')
const dialog = ref(false)
const loading = ref(false)
const saving = ref(false)
const packages = ref<PtPackage[]>([])
const sessions = ref<PtSession[]>([])
const newPkg = reactive({ member_id: 1, name: '', total_sessions: 10, remaining_sessions: 10, amount_cents: 0 })

async function load() {
  loading.value = true
  try {
    const [pkgRes, sessionRes] = await Promise.all([ptApi.listPackages(), ptApi.listSessions()])
    packages.value = pkgRes.data.items
    sessions.value = sessionRes.data.items
  } finally {
    loading.value = false
  }
}
async function createPackage() {
  saving.value = true
  try {
    await ptApi.createPackage(newPkg)
    ElMessage.success('新增成功')
    dialog.value = false
    Object.assign(newPkg, { member_id: 1, name: '', total_sessions: 10, remaining_sessions: 10, amount_cents: 0 })
    await load()
  } finally {
    saving.value = false
  }
}
onMounted(load)
</script>
