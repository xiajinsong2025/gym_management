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
}

