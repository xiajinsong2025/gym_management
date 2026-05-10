<template>
  <div>
    <v-card>
      <v-card-title>
        <h2>课程管理</h2>
      </v-card-title>
      <v-card-text>
        <v-tabs v-model="activeTab">
          <v-tab value="courses">课程列表</v-tab>
          <v-tab value="schedules">排期管理</v-tab>
          <v-tab value="bookings">预约记录</v-tab>
        </v-tabs>

        <v-window v-model="activeTab" class="mt-4">
          <v-window-item value="courses">
            <v-card flat>
              <v-card-text>
                <v-btn color="primary" class="mb-4">
                  <v-icon left>mdi-plus</v-icon>
                  新增课程
                </v-btn>
                <v-data-table
                  :headers="courseHeaders"
                  :items="courses"
                  :loading="loading"
                  hide-default-footer
                >
                  <template v-slot:item.default_capacity="{ item }">
                    <v-chip color="info" small>{{ item.default_capacity }}人</v-chip>
                  </template>
                  <template v-slot:item.duration_minutes="{ item }">
                    {{ item.duration_minutes }}分钟
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-window-item>

          <v-window-item value="schedules">
            <v-card flat>
              <v-card-text>
                <v-btn color="primary" class="mb-4">
                  <v-icon left>mdi-plus</v-icon>
                  新增排期
                </v-btn>
                <v-data-table
                  :headers="scheduleHeaders"
                  :items="schedules"
                  :loading="loading"
                  hide-default-footer
                >
                  <template v-slot:item.status="{ item }">
                    <v-chip :color="getScheduleStatusColor(item.status)" small>
                      {{ getScheduleStatusText(item.status) }}
                    </v-chip>
                  </template>
                  <template v-slot:item.capacity="{ item }">
                    {{ item.booked_count }}/{{ item.capacity }}
                    <v-chip v-if="item.waitlisted_count > 0" color="warning" x-small class="ml-1">
                      候补{{ item.waitlisted_count }}
                    </v-chip>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-window-item>

          <v-window-item value="bookings">
            <v-card flat>
              <v-card-text>
                <v-data-table
                  :headers="bookingHeaders"
                  :items="bookings"
                  :loading="loading"
                  hide-default-footer
                >
                  <template v-slot:item.status="{ item }">
                    <v-chip :color="getBookingStatusColor(item.status)" small>
                      {{ getBookingStatusText(item.status) }}
                    </v-chip>
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
import type { Course, CourseSchedule } from '@/types'

const loading = ref(false)
const activeTab = ref('courses')
const courses = ref<Course[]>([])
const schedules = ref<CourseSchedule[]>([])
const bookings = ref<any[]>([])

const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const courseHeaders = [
  { title: 'ID', key: 'id' },
  { title: '课程名称', key: 'name' },
  { title: '默认容量', key: 'default_capacity' },
  { title: '时长', key: 'duration_minutes' },
  { title: '描述', key: 'description' }
]

const scheduleHeaders = [
  { title: 'ID', key: 'id' },
  { title: '课程ID', key: 'course_id' },
  { title: '开始时间', key: 'start_time' },
  { title: '结束时间', key: 'end_time' },
  { title: '预约情况', key: 'capacity' },
  { title: '状态', key: 'status' }
]

const bookingHeaders = [
  { title: 'ID', key: 'id' },
  { title: '排期ID', key: 'schedule_id' },
  { title: '会员ID', key: 'member_id' },
  { title: '状态', key: 'status' },
  { title: '预约时间', key: 'created_at' }
]

function showSnackbar(text: string, color: string = 'success') {
  snackbarText.value = text
  snackbarColor.value = color
  snackbar.value = true
}

function getScheduleStatusText(status: string) {
  const statusMap: Record<string, string> = {
    scheduled: '已排期',
    cancelled: '已取消',
    finished: '已完成'
  }
  return statusMap[status] || status
}

function getScheduleStatusColor(status: string) {
  const colorMap: Record<string, string> = {
    scheduled: 'primary',
    cancelled: 'error',
    finished: 'success'
  }
  return colorMap[status] || 'grey'
}

function getBookingStatusText(status: string) {
  const statusMap: Record<string, string> = {
    booked: '已预约',
    cancelled: '已取消',
    attended: '已签到',
    waitlisted: '候补中'
  }
  return statusMap[status] || status
}

function getBookingStatusColor(status: string) {
  const colorMap: Record<string, string> = {
    booked: 'primary',
    cancelled: 'error',
    attended: 'success',
    waitlisted: 'warning'
  }
  return colorMap[status] || 'grey'
}

async function loadData() {
  loading.value = true
  try {
    // TODO: Implement API calls
    // Mock data
    courses.value = [
      {
        id: 1,
        name: '瑜伽课',
        default_capacity: 20,
        duration_minutes: 60,
        description: '基础瑜伽课程'
      },
      {
        id: 2,
        name: '动感单车',
        default_capacity: 30,
        duration_minutes: 45,
        description: '高强度有氧训练'
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
