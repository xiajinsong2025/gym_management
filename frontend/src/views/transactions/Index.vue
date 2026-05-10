<template>
  <div>
    <v-card>
      <v-card-title>
        <h2>卡务交易</h2>
      </v-card-title>
      <v-card-text>
        <v-tabs v-model="activeTab">
          <v-tab value="cardTypes">卡种管理</v-tab>
          <v-tab value="memberCards">会员卡管理</v-tab>
          <v-tab value="transactions">交易记录</v-tab>
        </v-tabs>

        <v-window v-model="activeTab" class="mt-4">
          <v-window-item value="cardTypes">
            <v-card flat>
              <v-card-text>
                <v-btn color="primary" class="mb-4">
                  <v-icon left>mdi-plus</v-icon>
                  新增卡种
                </v-btn>
                <v-data-table
                  :headers="cardTypeHeaders"
                  :items="cardTypes"
                  :loading="loading"
                  hide-default-footer
                >
                  <template v-slot:item.kind="{ item }">
                    <v-chip small>{{ getCardKindText(item.kind) }}</v-chip>
                  </template>
                  <template v-slot:item.price_cents="{ item }">
                    ¥{{ (item.price_cents / 100).toFixed(2) }}
                  </template>
                  <template v-slot:item.is_active="{ item }">
                    <v-chip :color="item.is_active ? 'success' : 'grey'" small>
                      {{ item.is_active ? '启用' : '禁用' }}
                    </v-chip>
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-window-item>

          <v-window-item value="memberCards">
            <v-card flat>
              <v-card-text>
                <v-btn color="primary" class="mb-4">
                  <v-icon left>mdi-plus</v-icon>
                  开卡
                </v-btn>
                <v-data-table
                  :headers="memberCardHeaders"
                  :items="memberCards"
                  :loading="loading"
                  hide-default-footer
                >
                  <template v-slot:item.status="{ item }">
                    <v-chip :color="getCardStatusColor(item.status)" small>
                      {{ getCardStatusText(item.status) }}
                    </v-chip>
                  </template>
                  <template v-slot:item.balance_cents="{ item }">
                    ¥{{ ((item.balance_cents || 0) / 100).toFixed(2) }}
                  </template>
                </v-data-table>
              </v-card-text>
            </v-card>
          </v-window-item>

          <v-window-item value="transactions">
            <v-card flat>
              <v-card-text>
                <v-data-table
                  :headers="transactionHeaders"
                  :items="transactions"
                  :loading="loading"
                  hide-default-footer
                >
                  <template v-slot:item.transaction_type="{ item }">
                    <v-chip small>{{ getTransactionTypeText(item.transaction_type) }}</v-chip>
                  </template>
                  <template v-slot:item.amount_cents="{ item }">
                    ¥{{ (item.amount_cents / 100).toFixed(2) }}
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
import type { CardType, MemberCard } from '@/types'

const loading = ref(false)
const activeTab = ref('cardTypes')
const cardTypes = ref<CardType[]>([])
const memberCards = ref<MemberCard[]>([])
const transactions = ref<any[]>([])

const snackbar = ref(false)
const snackbarText = ref('')
const snackbarColor = ref('success')

const cardTypeHeaders = [
  { title: 'ID', key: 'id' },
  { title: '卡种名称', key: 'name' },
  { title: '类型', key: 'kind' },
  { title: '价格', key: 'price_cents' },
  { title: '有效期(天)', key: 'validity_days' },
  { title: '次数', key: 'total_times' },
  { title: '状态', key: 'is_active' }
]

const memberCardHeaders = [
  { title: 'ID', key: 'id' },
  { title: '卡号', key: 'card_no' },
  { title: '类型', key: 'kind' },
  { title: '状态', key: 'status' },
  { title: '开始日期', key: 'start_date' },
  { title: '结束日期', key: 'end_date' },
  { title: '剩余次数', key: 'remaining_times' },
  { title: '余额', key: 'balance_cents' }
]

const transactionHeaders = [
  { title: 'ID', key: 'id' },
  { title: '交易类型', key: 'transaction_type' },
  { title: '金额', key: 'amount_cents' },
  { title: '次数变更', key: 'times_delta' },
  { title: '备注', key: 'note' },
  { title: '创建时间', key: 'created_at' }
]

function showSnackbar(text: string, color: string = 'success') {
  snackbarText.value = text
  snackbarColor.value = color
  snackbar.value = true
}

function getCardKindText(kind: string) {
  const kindMap: Record<string, string> = {
    time: '时间卡',
    times: '次卡',
    stored_value: '储值卡',
    personal_training: '私教卡'
  }
  return kindMap[kind] || kind
}

function getCardStatusText(status: string) {
  const statusMap: Record<string, string> = {
    active: '正常',
    frozen: '冻结',
    expired: '过期',
    refunded: '已退卡'
  }
  return statusMap[status] || status
}

function getCardStatusColor(status: string) {
  const colorMap: Record<string, string> = {
    active: 'success',
    frozen: 'warning',
    expired: 'error',
    refunded: 'grey'
  }
  return colorMap[status] || 'primary'
}

function getTransactionTypeText(type: string) {
  const typeMap: Record<string, string> = {
    open: '开卡',
    renew: '续费',
    recharge: '充值',
    consume: '消费',
    freeze: '冻结',
    unfreeze: '解冻',
    refund: '退卡',
    transfer: '转卡'
  }
  return typeMap[type] || type
}

async function loadData() {
  loading.value = true
  try {
    // TODO: Implement API calls
    // For now, use mock data
    cardTypes.value = [
      {
        id: 1,
        name: '年卡',
        kind: 'time',
        price_cents: 299900,
        validity_days: 365,
        is_active: true
      },
      {
        id: 2,
        name: '次卡(30次)',
        kind: 'times',
        price_cents: 199900,
        total_times: 30,
        is_active: true
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
