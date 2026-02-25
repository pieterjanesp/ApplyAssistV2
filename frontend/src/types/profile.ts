export interface Profile {
  id: string
  user_id: string
  full_name: string
  email: string
  phone?: string
  location?: string
  summary?: string
  skills: string[]
  experience_years?: number
  created_at: string
  updated_at: string
}

export interface ProfileCreate {
  full_name: string
  email: string
  phone?: string
  location?: string
  summary?: string
  skills?: string[]
  experience_years?: number
}

export type ProfileUpdate = Partial<ProfileCreate>
