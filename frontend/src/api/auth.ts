import { request } from './request'
import type { ApiResponse, LoginRequest, LoginResponse, User } from '@/types'

export const authApi = {
  login(data: LoginRequest): Promise<ApiResponse<LoginResponse>> {
    return request.post('/auth/login', data)
  },

  register(data: { username: string; password: string; display_name: string }): Promise<ApiResponse<User>> {
    return request.post('/auth/register', data)
  },

  grantPermissions(codes: string[]): Promise<ApiResponse<string[]>> {
    return request.post('/auth/me/permissions', { codes })
  }
}
