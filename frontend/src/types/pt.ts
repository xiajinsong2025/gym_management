export interface PtPackage {
  id: number
  member_id: number
  coach_id: number | null
  name: string
  total_sessions: number
  remaining_sessions: number
  amount_cents: number
  status: string
}

export interface PtSession {
  id: number
  package_id: number
  member_id: number
  coach_id: number
  start_time: string
  end_time: string
  status: 'scheduled' | 'confirmed' | 'cancelled'
  note?: string | null
}
