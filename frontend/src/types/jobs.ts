export interface Job {
  id: string
  title: string
  company: string
  location: string
  description: string
  requirements: string[]
  salary_range?: string
  job_type: string
  source_url?: string
  created_at: string
}

export interface JobCreate {
  title: string
  company: string
  location: string
  description: string
  requirements?: string[]
  salary_range?: string
  job_type?: string
  source_url?: string
}

export interface JobSearchParams {
  query?: string
  location?: string
  job_type?: string
}
