import { request } from './request'
import type { ApiResponse, PageResponse, Member, MemberCreate, MemberUpdate } from '@/types'

export const memberApi = {
  list(params: {
    keyword?: string
    status?: string
    page?: number
    page_size?: number
  }): Promise<ApiResponse<PageResponse<Member>>> {
    return request.get('/members', { params })
  },

  get(id: number): Promise<ApiResponse<Member>> {
    return request.get(`/members/${id}`)
  },

  create(data: MemberCreate): Promise<ApiResponse<Member>> {
    return request.post('/members', data)
  },

  update(id: number, data: MemberUpdate): Promise<ApiResponse<Member>> {
    return request.patch(`/members/${id}`, data)
  },

  delete(id: number): Promise<ApiResponse<void>> {
    return request.delete(`/members/${id}`)
  }
}
