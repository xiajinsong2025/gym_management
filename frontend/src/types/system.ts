export interface SystemUser {
  id: number
  username: string
  display_name: string
  mobile: string | null
  email: string | null
  is_active: boolean
  is_superuser: boolean
  created_at: string
  updated_at: string
}

export interface SystemRole {
  id: number
  name: string
  code: string
  description: string | null
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface SystemDepartment {
  id: number
  name: string
  parent_id: number | null
  sort_order: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface SystemMenu {
  id: number
  parent_id: number | null
  title: string
  path: string
  component: string | null
  icon: string | null
  permission_code: string | null
  sort_order: number
  is_visible: boolean
  created_at: string
  updated_at: string
}

export interface OperationLog {
  id: number
  user_id: number | null
  action: string
  resource: string | null
  method: string | null
  path: string | null
  ip_address: string | null
  detail: string | null
  created_at: string
  updated_at: string
}

export interface PermissionItem {
  id: number
  name: string
  code: string
  description: string | null
  created_at: string
  updated_at: string
}
