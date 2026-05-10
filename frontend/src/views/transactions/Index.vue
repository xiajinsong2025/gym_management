<template>
  <div class="page-card">
    <div class="page-header">
      <div class="page-title">卡务交易</div>
      <el-button type="primary" @click="dialog = true">新增卡种</el-button>
    </div>
    <div class="table-wrap">
      <el-tabs v-model="tab">
        <el-tab-pane label="卡种" name="types">
          <el-table :data="cardTypes" border v-loading="loading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="name" label="名称" />
            <el-table-column prop="kind" label="类型" />
            <el-table-column prop="price_cents" label="价格(分)" />
          </el-table>
        </el-tab-pane>
        <el-tab-pane label="会员卡" name="cards">
          <el-table :data="cards" border v-loading="loading">
            <el-table-column prop="id" label="ID" width="80" />
            <el-table-column prop="member_id" label="会员ID" />
            <el-table-column prop="card_no" label="卡号" />
            <el-table-column prop="status" label="状态" />
            <el-table-column prop="balance_cents" label="余额(分)" />
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </div>
  </div>

  <el-dialog v-model="dialog" title="新增卡种" width="520">
    <el-form :model="newType" label-position="top">
      <el-form-item label="名称"><el-input v-model="newType.name" /></el-form-item>
      <el-form-item label="类型"><el-select v-model="newType.kind"><el-option v-for="k in kinds" :key="k" :label="k" :value="k" /></el-select></el-form-item>
      <el-form-item label="价格(分)"><el-input-number v-model="newType.price_cents" :min="0" style="width: 100%" /></el-form-item>
    </el-form>
    <template #footer>
      <el-button @click="dialog = false">取消</el-button>
      <el-button type="primary" :loading="saving" @click="createType">保存</el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { transactionApi } from '@/api/business'
import type { CardKind, CardType, MemberCard } from '@/types'

const tab = ref('types')
const dialog = ref(false)
const loading = ref(false)
const saving = ref(false)
const cardTypes = ref<CardType[]>([])
const cards = ref<MemberCard[]>([])
const kinds: CardKind[] = ['time', 'times', 'stored_value', 'personal_training']
const newType = reactive({ name: '', kind: 'stored_value' as CardKind, price_cents: 0 })

async function load() {
  loading.value = true
  try {
    const [types, memberCards] = await Promise.all([transactionApi.listCardTypes(), transactionApi.listMemberCards()])
    cardTypes.value = types.data.items
    cards.value = memberCards.data.items
  } finally {
    loading.value = false
  }
}
async function createType() {
  saving.value = true
  try {
    await transactionApi.createCardType(newType)
    ElMessage.success('新增成功')
    dialog.value = false
    Object.assign(newType, { name: '', kind: 'stored_value', price_cents: 0 })
    await load()
  } finally {
    saving.value = false
  }
}
onMounted(load)
</script>
