export type CardKind = 'time' | 'times' | 'stored_value' | 'personal_training'
export type CardStatus = 'active' | 'frozen' | 'expired' | 'refunded'

export interface CardType {
  id: number
  name: string
  kind: CardKind
  price_cents: number
  validity_days: number | null
  total_times: number | null
  stored_value_cents: number | null
  is_active: boolean
  description: string | null
}

export interface MemberCard {
  id: number
  member_id: number
  card_type_id: number
  card_no: string
  kind: CardKind
  status: CardStatus
  start_date: string | null
  end_date: string | null
  remaining_times: number | null
  balance_cents: number | null
  frozen_from: string | null
  remark: string | null
}
