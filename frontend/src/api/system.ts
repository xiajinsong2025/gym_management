import { request } from './request'
import type { OperationLog, PageResponse, PermissionItem, SystemDepartment, SystemMenu, SystemRole, SystemUser } from '@/types'

export const systemApi = {
  listUsers(params?: { keyword?: string; page?: number; page_size?: number }) {
    return request.get<PageResponse<SystemUser>>('/system/users', { params })
  },
  createUser(data: {
    username: string
    password: string
    display_name: string
    mobile?: string | null
    email?: string | null
    is_active?: boolean
    is_superuser?: boolean
  }) {
    return request.post<SystemUser>('/system/users', data)
  },
  updateUser(userId: number, data: Partial<Pick<SystemUser, 'display_name' | 'mobile' | 'email' | 'is_active' | 'is_superuser'>>) {
    return request.patch<SystemUser>(`/system/users/${userId}`, data)
  },
  listRoles(params?: { page?: number; page_size?: number }) {
    return request.get<PageResponse<SystemRole>>('/system/roles', { params })
  },
  createRole(data: { name: string; code: string; description?: string | null; is_active?: boolean }) {
    return request.post<SystemRole>('/system/roles', data)
  },
  updateRole(roleId: number, data: Partial<Pick<SystemRole, 'name' | 'description' | 'is_active'>>) {
    return request.patch<SystemRole>(`/system/roles/${roleId}`, data)
  },
  listPermissions() {
    return request.get<PermissionItem[]>('/system/permissions')
  },
  getRolePermissions(roleId: number) {
    return request.get<string[]>(`/system/roles/${roleId}/permissions`)
  },
  updateRolePermissions(roleId: number, codes: string[]) {
    return request.put<string[]>(`/system/roles/${roleId}/permissions`, { codes })
  },
  listDepartments(params?: { page?: number; page_size?: number }) {
    return request.get<PageResponse<SystemDepartment>>('/system/departments', { params })
  },
  createDepartment(data: { name: string; parent_id?: number | null; sort_order?: number; is_active?: boolean }) {
    return request.post<SystemDepartment>('/system/departments', data)
  },
  updateDepartment(departmentId: number, data: Partial<Pick<SystemDepartment, 'name' | 'parent_id' | 'sort_order' | 'is_active'>>) {
    return request.patch<SystemDepartment>(`/system/departments/${departmentId}`, data)
  },
  listMenus(params?: { page?: number; page_size?: number }) {
    return request.get<PageResponse<SystemMenu>>('/system/menus', { params })
  },
  createMenu(data: {
    parent_id?: number | null
    title: string
    path: string
    component?: string | null
    icon?: string | null
    permission_code?: string | null
    sort_order?: number
    is_visible?: boolean
  }) {
    return request.post<SystemMenu>('/system/menus', data)
  },
  updateMenu(menuId: number, data: Partial<SystemMenu>) {
    return request.patch<SystemMenu>(`/system/menus/${menuId}`, data)
  },
  listOperationLogs(params?: { page?: number; page_size?: number }) {
    return request.get<PageResponse<OperationLog>>('/system/logs/operations', { params })
  },
}
