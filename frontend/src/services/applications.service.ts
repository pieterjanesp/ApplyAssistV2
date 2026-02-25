import api from '../lib/api'

export interface Application {
  id: string
  user_id: string
  job_id: string
  cv_id?: string
  cover_letter_id?: string
  status: 'draft' | 'applied' | 'interviewing' | 'offered' | 'rejected' | 'withdrawn'
  applied_at?: string
  notes?: string
  created_at: string
  updated_at: string
}

export interface ApplicationCreate {
  job_id: string
  cv_id?: string
  cover_letter_id?: string
  notes?: string
}

export interface ApplicationUpdate {
  status?: Application['status']
  notes?: string
}

export const applicationsService = {
  async createApplication(payload: ApplicationCreate): Promise<Application> {
    const { data } = await api.post<Application>('/api/v1/applications/', payload)
    return data
  },

  async listApplications(): Promise<Application[]> {
    const { data } = await api.get<Application[]>('/api/v1/applications/')
    return data
  },

  async getApplication(applicationId: string): Promise<Application> {
    const { data } = await api.get<Application>(`/api/v1/applications/${applicationId}`)
    return data
  },

  async updateApplication(
    applicationId: string,
    payload: ApplicationUpdate,
  ): Promise<Application> {
    const { data } = await api.patch<Application>(
      `/api/v1/applications/${applicationId}`,
      payload,
    )
    return data
  },
}
