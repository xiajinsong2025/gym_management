<template>
  <div>
    <v-card>
      <v-card-title>
        <h2>私教管理</h2>
      </v-card-title>
      <v-card-text>
        <v-tabs v-model="activeTab">
          <v-tab value="packages">私教课包</v-tab>
          <v-tab value="sessions">排课记录</v-tab>
        </v-tabs>

        <v-window v-model="activeTab" class="mt-4">
          <v-window-item value="packages">
            <v-card flat>
              <v-card-text>
                <v-btn color="primary" class="mb-4">
                  <v-icon left>mdi-plus</v-icon>
                  新增私教课包
                </v-btn>
                <v-data-table
                  :headers="packageHeaders"
                  :items="packages"
                  :loading="loading"
                  hide-default-footer
                >
                  <template v-slot:item.sessions="{ item }">
                    <v-chip color="info" small>
                      {{ item.used_sessions }}/{{ item.total_sessions }}
                    </v-chip>
                  </template>
                  <template v-slot:item.status="{ item }">
                    <v-chip :color="getPackageStatusColor(item.status)" small>
                      {{ getPackageStatusText(item.status) }}
                    </v-chip>
                  </template>
                  <template v-slot:item.actions="{ item }">
                    <v-btn small text color="primary">
                      <v-icon small>mdi-calendar-plus</v-icon>
                      排课
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-window-item>

          <v-window-item value="sessions">
            <v-card flat>
              <v-card-text>
                <v-data-table
                  :headers="sessionHeaders"
                  :items="sessions"
                  :loading="loading"
                  hide-default-footer
                >
                  <template v-slot:item.status="{ item }">
                    <v-chip :color="getSessionStatusColor(item.status)" small>
                      {{ getSessionStatusText(item.status) }}
                    </v-chip>
                  </template>
                  <template v-slot:item.actions="{ item }">
                    <v-btn small text color="success" v-if="item.status === 'scheduled'">
                      <v-icon small>mdi-check</v-icon>
                      确认
                    </v-btn>
                    <v-btn small text color="primary" v-if="item.status === 'confirmed'">
                      <v-icon small>mdi-check-all</v-icon>
                      消课
                    </v-btn>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </v-card-text>
    </v-card>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import type { PersonalTrainingPackage } from '@/types'

const loading = ref(false)
const activeTab = ref('packages')
const packages = ref<PersonalTrainingPackage[]>([])
const sessions = ref<any[]>([])

const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const packageHeaders = [
  { title: 'ID', key: 'id' },
  { title: '会员ID', key: 'member_id' },
  { title: '教练ID', key: 'coach_id' },
  { title: '总课时', key: 'total_sessions' },
  { title: '已用课时', key: 'used_sessions' },
  { title: '进度', key: 'sessions' },
  { title: '状态', key: 'status' },
  { title: '操作', key: 'actions', sortable: false }
]

const sessionHeaders = [
  { title: 'ID', key: 'id' },
  { title: '课包ID', key: 'package_id' },
  { title: '教练ID', key: 'coach_id' },
  { title: '预约时间', key: 'scheduled_at' },
  { title: '状态', key: 'status' },
  { title: '操作', key: 'actions', sortable: false }
]

function showSnackbar(text: string, color: string = 'success') {
  snackbarText.value = text
  snackbarColor.value = color
  snackbar.value = true
}

function getPackageStatusText(status: string) {
  const statusMap: Record<string, string> = {
    active: '进行中',
    finished: '已完成',
    expired: '已过期'
  }
  return statusMap[status] || status
}

function getPackageStatusColor(status: string) {
  const colorMap: Record<string, string> = {
    active: 'success',
    finished: 'info',
    expired: 'error'
  }
  return colorMap[status] || 'grey'
}

function getSessionStatusText(status: string) {
  const statusMap: Record<string, string> = {
    scheduled: '已排课',
    confirmed: '已确认',
    completed: '已消课',
    cancelled: '已取消'
  }
  return statusMap[status] || status
}

function getSessionStatusColor(status: string) {
  const colorMap: Record<string, string> = {
    scheduled: 'warning',
    confirmed: 'primary',
    completed: 'success',
    cancelled: 'error'
  }
  return colorMap[status] || 'grey'
}

async function loadData() {
  loading.value = true
  try {
    // TODO: Implement API calls
    // Mock data
    packages.value = [
      {
        id: 1,
        member_id: 1,
        coach_id: 1,
        total_sessions: 10,
        used_sessions: 3,
        status: 'active'
      }
    ]
  } catch (error: any) {
    showSnackbar(error.message || '加载数据失败', 'error')
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  loadData()
})
</script>
