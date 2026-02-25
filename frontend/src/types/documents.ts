export interface CVItem {
  id: string
  content: string
  order: number
}

export interface CVSection {
  id: string
  title: string
  section_type: 'experience' | 'education' | 'skills' | 'projects' | 'certifications' | 'custom'
  items: CVItem[]
  order: number
}

export interface CV {
  id: string
  user_id: string
  title: string
  sections: CVSection[]
  created_at: string
  updated_at: string
}

export interface CoverLetter {
  id: string
  user_id: string
  job_id?: string
  content: string
  tone: string
  created_at: string
  updated_at: string
}

export interface CVGenerateRequest {
  job_description?: string
  target_role?: string
}

export interface CVAdaptRequest {
  cv_id: string
  job_description: string
}

export interface CVOptimiseRequest {
  cv_id: string
  instructions?: string
}

export interface CoverLetterGenerateRequest {
  job_id?: string
  job_description?: string
  tone?: string
}
