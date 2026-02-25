import api from '../lib/api'
import type { Profile, ProfileCreate, ProfileUpdate } from '../types/profile'

export const profileService = {
  async getProfile(): Promise<Profile> {
    const { data } = await api.get<Profile>('/api/v1/profile/')
    return data
  },

  async createProfile(payload: ProfileCreate): Promise<Profile> {
    const { data } = await api.post<Profile>('/api/v1/profile/', payload)
    return data
  },

  async updateProfile(payload: ProfileUpdate): Promise<Profile> {
    const { data } = await api.patch<Profile>('/api/v1/profile/', payload)
    return data
  },

  async extractInfo(): Promise<Profile> {
    const { data } = await api.post<Profile>('/api/v1/profile/extract')
    return data
  },
}
