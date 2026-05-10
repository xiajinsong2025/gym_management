<template>
  <div class="page-card">
    <div class="page-header">
      <div class="page-title">操作日志</div>
    </div>
    <div class="table-wrap">
      <el-table :data="rows" border v-loading="loading">
        <el-table-column prop="id" label="ID" width="72" />
        <el-table-column prop="user_id" label="用户ID" width="90" />
        <el-table-column prop="action" label="动作" width="150" />
        <el-table-column prop="resource" label="资源" width="120" />
        <el-table-column prop="method" label="方法" width="90" />
        <el-table-column prop="path" label="路径" />
        <el-table-column prop="ip_address" label="IP" width="140" />
        <el-table-column prop="created_at" label="时间" width="190" />
      </el-table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { systemApi } from '@/api/system'
import type { OperationLog } from '@/types'

const rows = ref<OperationLog[]>([])
const loading = ref(false)

async function load() {
  loading.value = true
  try {
    const res = await systemApi.listOperationLogs()
    rows.value = res.data.items
  } finally {
    loading.value = false
  }
}
onMounted(load)
</script>
