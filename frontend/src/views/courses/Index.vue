<template>
  <div class="page-card">
    <div class="page-header">
      <div class="page-title">课程管理</div>
      <el-button type="primary" @click="dialog = true">新增课程</el-button>
    </div>
    <div class="table-wrap">
      <el-tabs v-model="tab">
        <el-tab-pane label="课程" name="courses">
          <el-table :data="courses" border v-loading="loading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="default_capacity" label="容量" />
            <el-table-column prop="duration_minutes" label="时长(分)" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="排期" name="schedules">
          <el-table :data="schedules" border v-loading="loading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="course_id" label="课程ID" />
            <el-table-column prop="start_time" label="开始时间" />
            <el-table-column prop="status" label="状态" />
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>

  <el-dialog v-model="dialog" title="新增课程" width="520">
    <el-form :model="newCourse" label-position="top">
      <el-form-item label="名称"><el-input v-model="newCourse.name" /></el-form-item>
      <el-form-item label="默认容量"><el-input-number v-model="newCourse.default_capacity" :min="0" style="width: 100%" /></el-form-item>
      <el-form-item label="时长(分)"><el-input-number v-model="newCourse.duration_minutes" :min="1" style="width: 100%" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialog = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="createCourse">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { courseApi } from '@/api/business'
import type { Course, CourseSchedule } from '@/types'

const tab = ref('courses')
const dialog = ref(false)
const loading = ref(false)
const saving = ref(false)
const courses = ref<Course[]>([])
const schedules = ref<CourseSchedule[]>([])
const newCourse = reactive({ name: '', default_capacity: 20, duration_minutes: 60 })

async function load() {
  loading.value = true
  try {
    const [courseRes, scheduleRes] = await Promise.all([courseApi.listCourses(), courseApi.listSchedules()])
    courses.value = courseRes.data.items
    schedules.value = scheduleRes.data.items
  } finally {
    loading.value = false
  }
}
async function createCourse() {
  saving.value = true
  try {
    await courseApi.createCourse(newCourse)
    ElMessage.success('新增成功')
    dialog.value = false
    Object.assign(newCourse, { name: '', default_capacity: 20, duration_minutes: 60 })
    await load()
  } finally {
    saving.value = false
  }
}
onMounted(load)
</script>
