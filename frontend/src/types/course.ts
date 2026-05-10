export interface Course {
  id: number
  category_id: number | null
  name: string
  default_capacity: number
  duration_minutes: number
  description: string | null
}

export interface CourseSchedule {
  id: number
  course_id: number
  coach_id: number | null
  venue_id: number | null
  start_time: string
  end_time: string
  capacity: number
  booked_count: number
  waitlisted_count: number
  status: 'scheduled' | 'cancelled' | 'finished'
}
