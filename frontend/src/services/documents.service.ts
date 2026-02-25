import api from '../lib/api'
import type {
  CV,
  CVGenerateRequest,
  CVAdaptRequest,
  CVOptimiseRequest,
  CoverLetter,
  CoverLetterGenerateRequest,
} from '../types/documents'

export const documentsService = {
  async generateCV(payload: CVGenerateRequest): Promise<CV> {
    const { data } = await api.post<CV>('/api/v1/documents/cv/generate', payload)
    return data
  },

  async adaptCV(payload: CVAdaptRequest): Promise<CV> {
    const { data } = await api.post<CV>('/api/v1/documents/cv/adapt', payload)
    return data
  },

  async optimiseCV(payload: CVOptimiseRequest): Promise<CV> {
    const { data } = await api.post<CV>('/api/v1/documents/cv/optimise', payload)
    return data
  },

  async listCVs(): Promise<CV[]> {
    const { data } = await api.get<CV[]>('/api/v1/documents/cv/')
    return data
  },

  async getCV(cvId: string): Promise<CV> {
    const { data } = await api.get<CV>(`/api/v1/documents/cv/${cvId}`)
    return data
  },

  async generateCoverLetter(payload: CoverLetterGenerateRequest): Promise<CoverLetter> {
    const { data } = await api.post<CoverLetter>(
      '/api/v1/documents/cover-letter/generate',
      payload,
    )
    return data
  },

  async listCoverLetters(): Promise<CoverLetter[]> {
    const { data } = await api.get<CoverLetter[]>('/api/v1/documents/cover-letter/')
    return data
  },
}
