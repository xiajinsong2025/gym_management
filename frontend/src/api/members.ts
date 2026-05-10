import { request } from './request'
import type { Member, MemberCreate, MemberUpdate, PageResponse } from '@/types'

export const memberApi = {
  list(params?: { keyword?: string; status?: string; page?: number; page_size?: number }) {
    return request.get<PageResponse<Member>>('/members', { params })
  },
  create(data: MemberCreate) {
    return request.post<Member>('/members', data)
  },
  update(id: number, data: MemberUpdate) {
    return request.patch<Member>(`/members/${id}`, data)
  },
}

