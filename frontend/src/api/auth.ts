import { request } from './request'
import type { LoginRequest, LoginResponse } from '@/types'

export const authApi = {
  login(data: LoginRequest) {
    return request.post<LoginResponse>('/auth/login', data)
  },
  register(data: { username: string; password: string; display_name: string }) {
    return request.post('/auth/register', data)
  },
  grantPermissions(codes: string[]) {
    return request.post<string[]>('/auth/me/permissions', { codes })
  },
}

