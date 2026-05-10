export type Gender = 'unknown' | 'male' | 'female'
export type MemberStatus = 'normal' | 'frozen' | 'expired' | 'lost' | 'lead'

export interface Member {
  id: number
  name: string
  mobile: string
  member_no: string | null
  gender: Gender
  birthday: string | null
  status: MemberStatus
  source: string | null
  remark: string | null
  created_at: string
  updated_at: string
}

export interface MemberCreate {
  name: string
  mobile: string
  member_no?: string | null
  gender?: Gender
  birthday?: string | null
  source?: string | null
  remark?: string | null
}

export interface MemberUpdate {
  name?: string
  mobile?: string
  member_no?: string | null
  gender?: Gender
  birthday?: string | null
  status?: MemberStatus
  source?: string | null
  remark?: string | null
}
