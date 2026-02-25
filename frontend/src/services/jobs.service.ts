import api from '../lib/api'
import type { Job, JobCreate, JobSearchParams } from '../types/jobs'

export const jobsService = {
  async listJobs(params?: JobSearchParams): Promise<Job[]> {
    const { data } = await api.get<Job[]>('/api/v1/jobs/', { params })
    return data
  },

  async getJob(jobId: string): Promise<Job> {
    const { data } = await api.get<Job>(`/api/v1/jobs/${jobId}`)
    return data
  },

  async createJob(payload: JobCreate): Promise<Job> {
    const { data } = await api.post<Job>('/api/v1/jobs/', payload)
    return data
  },

  async getMatchedJobs(): Promise<Job[]> {
    const { data } = await api.get<Job[]>('/api/v1/jobs/match/profile')
    return data
  },
}
