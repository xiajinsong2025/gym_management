<template>
  <div>
    <v-card>
      <v-card-title>
        <v-row align="center">
          <v-col cols="12" sm="6">
            <h2>会员管理</h2>
          </v-col>
          <v-col cols="12" sm="6" class="text-right">
            <v-btn color="primary" @click="openCreateDialog">
              <v-icon left>mdi-plus</v-icon>
              新增会员
            </v-btn>
          </v-col>
        </v-row>
      </v-card-title>

      <v-card-text>
        <v-row class="mb-4">
          <v-col cols="12" sm="4">
            <v-text-field
              v-model="search"
              prepend-inner-icon="mdi-magnify"
              label="搜索会员(姓名/手机号)"
              clearable
              @keyup.enter="handleSearch"
            ></v-text-field>
          </v-col>
          <v-col cols="12" sm="3">
            <v-select
              v-model="statusFilter"
              :items="statusOptions"
              label="状态筛选"
              clearable
              @change="handleSearch"
            ></v-select>
          </v-col>
        </v-row>

        <v-data-table
          :headers="headers"
          :items="members"
          :loading="loading"
          :items-per-page="pageSize"
          hide-default-footer
          class="elevation-1"
        >
          <template v-slot:item.status="{ item }">
            <v-chip :color="getStatusColor(item.status)" small>
              {{ getStatusText(item.status) }}
            </v-chip>
          </template>

          <template v-slot:item.gender="{ item }">
            {{ getGenderText(item.gender) }}
          </template>

          <template v-slot:item.actions="{ item }">
            <v-btn small text color="primary" @click="viewMember(item)">
              <v-icon small>mdi-eye</v-icon>
              查看
            </v-btn>
            <v-btn small text color="primary" @click="editMember(item)">
              <v-icon small>mdi-pencil</v-icon>
              编辑
            </v-btn>
          </template>
        </v-data-table>

        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="7"
          @update:modelValue="loadMembers"
          class="mt-4"
        ></v-pagination>
      </v-card-text>
    </v-card>

    <!-- 创建/编辑对话框 -->
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title>
          <span class="text-h5">{{ editMode ? '编辑会员' : '新增会员' }}</span>
        </v-card-title>

        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-row>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="memberForm.name"
                  label="姓名 *"
                  :rules="[rules.required]"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="memberForm.mobile"
                  label="手机号 *"
                  :rules="[rules.required]"
                  required
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="memberForm.member_no"
                  label="会员编号"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="memberForm.gender"
                  :items="genderOptions"
                  label="性别"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="memberForm.birthday"
                  label="生日"
                  type="date"
                ></v-text-field>
              </v-col>
              <v-col cols="12" sm="6">
                <v-select
                  v-model="memberForm.status"
                  :items="statusOptions"
                  label="状态"
                ></v-select>
              </v-col>
              <v-col cols="12" sm="6">
                <v-text-field
                  v-model="memberForm.source"
                  label="来源"
                ></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-textarea
                  v-model="memberForm.remark"
                  label="备注"
                  rows="2"
                ></v-textarea>
              </v-col>
            </v-row>
          </v-form>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="dialog = false">取消</v-btn>
          <v-btn color="primary" :loading="saving" @click="saveMember">
            保存
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 查看详情对话框 -->
    <v-dialog v-model="viewDialog" max-width="800px">
      <v-card v-if="selectedMember">
        <v-card-title>
          <span class="text-h5">会员详情</span>
        </v-card-title>

        <v-card-text>
          <v-row>
            <v-col cols="6">
              <div class="mb-2"><strong>姓名：</strong>{{ selectedMember.name }}</div>
              <div class="mb-2"><strong>手机号：</strong>{{ selectedMember.mobile }}</div>
              <div class="mb-2"><strong>会员编号：</strong>{{ selectedMember.member_no || '-' }}</div>
              <div class="mb-2"><strong>性别：</strong>{{ getGenderText(selectedMember.gender) }}</div>
              <div class="mb-2"><strong>生日：</strong>{{ selectedMember.birthday || '-' }}</div>
            </v-col>
            <v-col cols="6">
              <div class="mb-2">
                <strong>状态：</strong>
                <v-chip :color="getStatusColor(selectedMember.status)" small>
                  {{ getStatusText(selectedMember.status) }}
                </v-chip>
              </div>
              <div class="mb-2"><strong>来源：</strong>{{ selectedMember.source || '-' }}</div>
              <div class="mb-2"><strong>创建时间：</strong>{{ selectedMember.created_at || '-' }}</div>
              <div class="mb-2"><strong>更新时间：</strong>{{ selectedMember.updated_at || '-' }}</div>
            </v-col>
            <v-col cols="12">
              <div class="mb-2"><strong>备注：</strong></div>
              <div>{{ selectedMember.remark || '-' }}</div>
            </v-col>
          </v-row>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="viewDialog = false">关闭</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- 消息提示 -->
    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
    </v-snackbar>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import { memberApi } from '@/api/members'
import type { Member, MemberCreate, MemberUpdate } from '@/types'

const loading = ref(false)
const saving = ref(false)
const dialog = ref(false)
const viewDialog = ref(false)
const editMode = ref(false)
const valid = ref(false)
const search = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(20)
const totalMembers = ref(0)
const members = ref<Member[]>([])
const selectedMember = ref<Member | null>(null)
const form = ref()

const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const memberForm = reactive<MemberCreate>({
  name: '',
  mobile: '',
  member_no: '',
  gender: 'unknown',
  birthday: '',
  status: 'normal',
  source: '',
  remark: ''
})

const rules = {
  required: (value: string) => !!value || '此字段为必填项'
}

const headers = [
  { title: 'ID', key: 'id', align: 'start' },
  { title: '姓名', key: 'name', align: 'start' },
  { title: '手机号', key: 'mobile', align: 'start' },
  { title: '会员编号', key: 'member_no', align: 'start' },
  { title: '性别', key: 'gender', align: 'start' },
  { title: '状态', key: 'status', align: 'start' },
  { title: '来源', key: 'source', align: 'start' },
  { title: '操作', key: 'actions', align: 'center', sortable: false }
]

const statusOptions = [
  { title: '正常', value: 'normal' },
  { title: '冻结', value: 'frozen' },
  { title: '过期', value: 'expired' },
  { title: '流失', value: 'lost' },
  { title: '潜在客户', value: 'lead' }
]

const genderOptions = [
  { title: '未知', value: 'unknown' },
  { title: '男', value: 'male' },
  { title: '女', value: 'female' }
]

const totalPages = computed(() => Math.ceil(totalMembers.value / pageSize.value))

function showSnackbar(text: string, color: string = 'success') {
  snackbarText.value = text
  snackbarColor.value = color
  snackbar.value = true
}

function getStatusText(status: string) {
  const statusMap: Record<string, string> = {
    normal: '正常',
    frozen: '冻结',
    expired: '过期',
    lost: '流失',
    lead: '潜在客户'
  }
  return statusMap[status] || status
}

function getStatusColor(status: string) {
  const colorMap: Record<string, string> = {
    normal: 'success',
    frozen: 'warning',
    expired: 'error',
    lost: 'grey',
    lead: 'info'
  }
  return colorMap[status] || 'primary'
}

function getGenderText(gender: string) {
  const genderMap: Record<string, string> = {
    unknown: '未知',
    male: '男',
    female: '女'
  }
  return genderMap[gender] || gender
}

async function loadMembers() {
  loading.value = true
  try {
    const response = await memberApi.list({
      keyword: search.value || undefined,
      status: statusFilter.value || undefined,
      page: currentPage.value,
      page_size: pageSize.value
    })

    if (response.code === 0 && response.data) {
      members.value = response.data.items
      totalMembers.value = response.data.total
    }
  } catch (error: any) {
    showSnackbar(error.message || '加载会员列表失败', 'error')
  } finally {
    loading.value = false
  }
}

function handleSearch() {
  currentPage.value = 1
  loadMembers()
}

function openCreateDialog() {
  editMode.value = false
  resetForm()
  dialog.value = true
}

function editMember(member: Member) {
  editMode.value = true
  Object.assign(memberForm, {
    name: member.name,
    mobile: member.mobile,
    member_no: member.member_no || '',
    gender: member.gender,
    birthday: member.birthday || '',
    status: member.status,
    source: member.source || '',
    remark: member.remark || ''
  })
  selectedMember.value = member
  dialog.value = true
}

function viewMember(member: Member) {
  selectedMember.value = member
  viewDialog.value = true
}

function resetForm() {
  Object.assign(memberForm, {
    name: '',
    mobile: '',
    member_no: '',
    gender: 'unknown',
    birthday: '',
    status: 'normal',
    source: '',
    remark: ''
  })
  if (form.value) {
    form.value.resetValidation()
  }
}

async function saveMember() {
  if (!valid.value) return

  saving.value = true
  try {
    let response
    if (editMode.value && selectedMember.value) {
      response = await memberApi.update(selectedMember.value.id, memberForm)
    } else {
      response = await memberApi.create(memberForm)
    }

    if (response.code === 0) {
      showSnackbar(editMode.value ? '会员更新成功' : '会员创建成功')
      dialog.value = false
      loadMembers()
    } else {
      showSnackbar(response.message || '操作失败', 'error')
    }
  } catch (error: any) {
    showSnackbar(error.message || '操作失败', 'error')
  } finally {
    saving.value = false
  }
}

onMounted(() => {
  loadMembers()
})
</script>
