export interface ApiResponse<T = any> {
  code: number
  message: string
  data: T
}

export interface PageResponse<T = any> {
  items: T[]
  total: number
  page: number
  page_size: number
}

export interface User {
  id: number
  username: string
  display_name: string
  mobile?: string
  email?: string
  is_active: boolean
  is_superuser: boolean
}

export interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access_token: string
}

export interface Member {
  id: number
  name: string
  mobile: string
  member_no?: string
  gender: 'unknown' | 'male' | 'female'
  birthday?: string
  status: 'normal' | 'frozen' | 'expired' | 'lost' | 'lead'
  source?: string
  consultant_id?: number
  coach_id?: number
  remark?: string
  created_at?: string
  updated_at?: string
}

export interface MemberCreate {
  name: string
  mobile: string
  member_no?: string
  gender?: 'unknown' | 'male' | 'female'
  birthday?: string
  status?: 'normal' | 'frozen' | 'expired' | 'lost' | 'lead'
  source?: string
  consultant_id?: number
  coach_id?: number
  remark?: string
}

export interface MemberUpdate {
  name?: string
  mobile?: string
  member_no?: string
  gender?: 'unknown' | 'male' | 'female'
  birthday?: string
  status?: 'normal' | 'frozen' | 'expired' | 'lost' | 'lead'
  source?: string
  consultant_id?: number
  coach_id?: number
  remark?: string
}

export interface CardType {
  id: number
  name: string
  kind: 'time' | 'times' | 'stored_value' | 'personal_training'
  price_cents: number
  validity_days?: number
  total_times?: number
  stored_value_cents?: number
  is_active: boolean
  description?: string
}

export interface MemberCard {
  id: number
  member_id: number
  card_type_id: number
  card_no: string
  kind: 'time' | 'times' | 'stored_value' | 'personal_training'
  status: 'active' | 'frozen' | 'expired' | 'refunded'
  start_date?: string
  end_date?: string
  remaining_times?: number
  balance_cents?: number
  frozen_from?: string
  remark?: string
}

export interface Course {
  id: number
  category_id?: number
  name: string
  default_capacity: number
  duration_minutes: number
  description?: string
}

export interface CourseSchedule {
  id: number
  course_id: number
  coach_id?: number
  venue_id?: number
  start_time: string
  end_time: string
  capacity: number
  booked_count: number
  waitlisted_count: number
  status: 'scheduled' | 'cancelled' | 'finished'
}

export interface PersonalTrainingPackage {
  id: number
  member_id: number
  coach_id?: number
  total_sessions: number
  used_sessions: number
  start_date?: string
  end_date?: string
  status: 'active' | 'finished' | 'expired'
  remark?: string
}