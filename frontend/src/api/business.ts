import { request } from './request'
import type { CardType, Course, CourseSchedule, MemberCard, PageResponse, PtPackage, PtSession } from '@/types'

export const transactionApi = {
  listCardTypes() {
    return request.get<PageResponse<CardType>>('/card-types')
  },
  createCardType(data: { name: string; kind: string; price_cents: number }) {
    return request.post<CardType>('/card-types', data)
  },
  listMemberCards(params?: { member_id?: number; page?: number; page_size?: number }) {
    return request.get<PageResponse<MemberCard>>('/member-cards', { params })
  },
}

export const courseApi = {
  listCourses(params?: { page?: number; page_size?: number }) {
    return request.get<PageResponse<Course>>('/courses', { params })
  },
  createCourse(data: {
    category_id?: number | null
    name: string
    default_capacity: number
    duration_minutes: number
    description?: string
  }) {
    return request.post<Course>('/courses', data)
  },
  listSchedules(params?: { page?: number; page_size?: number; course_id?: number }) {
    return request.get<PageResponse<CourseSchedule>>('/course-schedules', { params })
  },
}

export const ptApi = {
  listPackages(params?: { page?: number; page_size?: number; member_id?: number }) {
    return request.get<PageResponse<PtPackage>>('/pt/packages', { params })
  },
  createPackage(data: {
    member_id: number
    name: string
    total_sessions: number
    remaining_sessions: number
    amount_cents: number
  }) {
    return request.post<PtPackage>('/pt/packages', data)
  },
  listSessions(params?: { page?: number; page_size?: number; member_id?: number }) {
    return request.get<PageResponse<PtSession>>('/pt/sessions', { params })
  },
  createSession(data: { package_id: number; member_id: number; coach_id: number; start_time: string; end_time: string; note?: string }) {
    return request.post<PtSession>('/pt/sessions', data)
  },
  confirmSession(sessionId: number, confirmed_by_id?: number) {
    return request.post<PtSession>(`/pt/sessions/${sessionId}/confirm`, null, { params: { confirmed_by_id } })
  },
  consumeSession(sessionId: number, training_record_id?: number) {
    return request.post<PtSession>(`/pt/sessions/${sessionId}/consume`, null, { params: { training_record_id } })
  },
  rescheduleSession(sessionId: number, data: { start_time: string; end_time: string; note?: string }) {
    return request.post<PtSession>(`/pt/sessions/${sessionId}/reschedule`, data)
  },
  cancelSession(sessionId: number, note?: string) {
    return request.post<PtSession>(`/pt/sessions/${sessionId}/cancel`, { note })
  },
  packageRemaining(packageId: number) {
    return request.get<{ package_id: number; member_id: number; total_sessions: number; remaining_sessions: number; consumed_sessions: number }>(`/pt/packages/${packageId}/remaining`)
  },
  coachPerformance(coachId: number, params?: { start_at?: string; end_at?: string; commission_rate?: number }) {
    return request.get<{ coach_id: number; total_confirmed_sessions: number; total_consumed_sessions: number; total_amount_cents: number; commission_rate: number; commission_amount_cents: number }>(`/pt/coaches/${coachId}/performance`, { params })
  },
}
