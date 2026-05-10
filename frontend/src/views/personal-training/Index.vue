<template>
  <div class="page-card">
    <div class="page-header">
      <div class="page-title">私教管理</div>
      <div style="display:flex;gap:8px">
        <el-button @click="sessionDialog = true">新增排课</el-button>
        <el-button type="primary" @click="packageDialog = true">新增课包</el-button>
      </div>
    </div>
    <div class="table-wrap">
      <el-tabs v-model="tab">
        <el-tab-pane label="课包" name="packages">
          <el-table :data="packages" border v-loading="loading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="member_id" label="会员ID" width="100" />
            <el-table-column prop="coach_id" label="教练ID" width="100" />
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="total_sessions" label="总课时" width="100" />
            <el-table-column prop="remaining_sessions" label="剩余课时" width="100" />
            <el-table-column label="操作" width="110">
              <template #default="scope">
                <el-button link type="primary" @click="showRemaining(scope.row.id)">剩余明细</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="排课" name="sessions">
          <el-table :data="sessions" border v-loading="loading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="package_id" label="课包ID" width="100" />
            <el-table-column prop="member_id" label="会员ID" width="100" />
            <el-table-column prop="coach_id" label="教练ID" width="100" />
            <el-table-column prop="start_time" label="开始时间" width="180" />
            <el-table-column prop="end_time" label="结束时间" width="180" />
            <el-table-column prop="status" label="状态" width="120" />
            <el-table-column label="操作" width="260">
              <template #default="scope">
                <el-button link type="primary" @click="confirmSession(scope.row.id)">确认</el-button>
                <el-button link @click="openReschedule(scope.row)">改约</el-button>
                <el-button link @click="cancelSession(scope.row.id)">取消</el-button>
                <el-button link type="success" @click="consumeSession(scope.row.id)">消课</el-button>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="业绩统计" name="performance">
          <el-form :inline="true">
            <el-form-item label="教练ID"><el-input-number v-model="performanceForm.coach_id" :min="1" :controls="false" /></el-form-item>
            <el-form-item label="提成比例"><el-input-number v-model="performanceForm.commission_rate" :min="0" :max="1" :step="0.05" :precision="2" /></el-form-item>
            <el-form-item><el-button type="primary" @click="loadPerformance">查询</el-button></el-form-item>
          </el-form>
          <el-descriptions v-if="performance" :column="2" border>
            <el-descriptions-item label="教练ID">{{ performance.coach_id }}</el-descriptions-item>
            <el-descriptions-item label="确认课次">{{ performance.total_confirmed_sessions }}</el-descriptions-item>
            <el-descriptions-item label="消课课次">{{ performance.total_consumed_sessions }}</el-descriptions-item>
            <el-descriptions-item label="总销售额(分)">{{ performance.total_amount_cents }}</el-descriptions-item>
            <el-descriptions-item label="提成比例">{{ performance.commission_rate }}</el-descriptions-item>
            <el-descriptions-item label="提成金额(分)">{{ performance.commission_amount_cents }}</el-descriptions-item>
          </el-descriptions>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>

  <el-dialog v-model="packageDialog" title="新增私教课包" width="520">
    <el-form :model="newPkg" label-position="top">
      <el-form-item label="会员ID"><el-input-number v-model="newPkg.member_id" :min="1" style="width: 100%" /></el-form-item>
      <el-form-item label="教练ID"><el-input-number v-model="newPkg.coach_id" :min="1" style="width: 100%" /></el-form-item>
      <el-form-item label="名称"><el-input v-model="newPkg.name" /></el-form-item>
      <el-form-item label="总课时"><el-input-number v-model="newPkg.total_sessions" :min="1" style="width: 100%" /></el-form-item>
      <el-form-item label="剩余课时"><el-input-number v-model="newPkg.remaining_sessions" :min="0" style="width: 100%" /></el-form-item>
      <el-form-item label="金额(分)"><el-input-number v-model="newPkg.amount_cents" :min="0" style="width: 100%" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="packageDialog = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="createPackage">保存</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="sessionDialog" title="新增排课" width="520">
    <el-form :model="newSession" label-position="top">
      <el-form-item label="课包ID"><el-input-number v-model="newSession.package_id" :min="1" style="width: 100%" /></el-form-item>
      <el-form-item label="会员ID"><el-input-number v-model="newSession.member_id" :min="1" style="width: 100%" /></el-form-item>
      <el-form-item label="教练ID"><el-input-number v-model="newSession.coach_id" :min="1" style="width: 100%" /></el-form-item>
      <el-form-item label="开始时间"><el-date-picker v-model="newSession.start_time" type="datetime" value-format="YYYY-MM-DDTHH:mm:ssZ" style="width:100%" /></el-form-item>
      <el-form-item label="结束时间"><el-date-picker v-model="newSession.end_time" type="datetime" value-format="YYYY-MM-DDTHH:mm:ssZ" style="width:100%" /></el-form-item>
      <el-form-item label="备注"><el-input v-model="newSession.note" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="sessionDialog = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="createSession">保存</el-button>
    </template>
  </el-dialog>

  <el-dialog v-model="rescheduleDialog" title="改约排课" width="520">
    <el-form :model="rescheduleForm" label-position="top">
      <el-form-item label="开始时间"><el-date-picker v-model="rescheduleForm.start_time" type="datetime" value-format="YYYY-MM-DDTHH:mm:ssZ" style="width:100%" /></el-form-item>
      <el-form-item label="结束时间"><el-date-picker v-model="rescheduleForm.end_time" type="datetime" value-format="YYYY-MM-DDTHH:mm:ssZ" style="width:100%" /></el-form-item>
      <el-form-item label="备注"><el-input v-model="rescheduleForm.note" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="rescheduleDialog = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="submitReschedule">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { ptApi } from '@/api/business'
import type { PtPackage, PtSession } from '@/types'

const tab = ref('packages')
const packageDialog = ref(false)
const sessionDialog = ref(false)
const rescheduleDialog = ref(false)
const loading = ref(false)
const saving = ref(false)
const packages = ref<PtPackage[]>([])
const sessions = ref<PtSession[]>([])
const performance = ref<{ coach_id: number; total_confirmed_sessions: number; total_consumed_sessions: number; total_amount_cents: number; commission_rate: number; commission_amount_cents: number }>()
const rescheduleId = ref<number>()

const newPkg = reactive({ member_id: 1, coach_id: 1, name: '', total_sessions: 10, remaining_sessions: 10, amount_cents: 0 })
const newSession = reactive({ package_id: 1, member_id: 1, coach_id: 1, start_time: '', end_time: '', note: '' })
const rescheduleForm = reactive({ start_time: '', end_time: '', note: '' })
const performanceForm = reactive({ coach_id: 1, commission_rate: 0.3 })

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
    ElMessage.success('课包新增成功')
    packageDialog.value = false
    await load()
  } finally {
    saving.value = false
  }
}
async function createSession() {
  saving.value = true
  try {
    await ptApi.createSession(newSession)
    ElMessage.success('排课新增成功')
    sessionDialog.value = false
    await load()
  } finally {
    saving.value = false
  }
}
function openReschedule(row: PtSession) {
  rescheduleId.value = row.id
  rescheduleForm.start_time = row.start_time
  rescheduleForm.end_time = row.end_time
  rescheduleForm.note = row.note || ''
  rescheduleDialog.value = true
}
async function submitReschedule() {
  if (!rescheduleId.value) return
  saving.value = true
  try {
    await ptApi.rescheduleSession(rescheduleId.value, rescheduleForm)
    ElMessage.success('改约成功')
    rescheduleDialog.value = false
    await load()
  } finally {
    saving.value = false
  }
}
async function confirmSession(id: number) {
  await ptApi.confirmSession(id)
  ElMessage.success('已确认')
  await load()
}
async function cancelSession(id: number) {
  await ptApi.cancelSession(id, '手动取消')
  ElMessage.success('已取消')
  await load()
}
async function consumeSession(id: number) {
  await ptApi.consumeSession(id)
  ElMessage.success('已消课')
  await load()
}
async function showRemaining(packageId: number) {
  const res = await ptApi.packageRemaining(packageId)
  ElMessage.info(`课包${res.data.package_id} 剩余${res.data.remaining_sessions}/${res.data.total_sessions}`)
}
async function loadPerformance() {
  const res = await ptApi.coachPerformance(performanceForm.coach_id, { commission_rate: performanceForm.commission_rate })
  performance.value = res.data
}
onMounted(load)
</script>
