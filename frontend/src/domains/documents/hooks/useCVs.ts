import { useCallback, useState } from 'react'
import { documentsService } from '../../../services/documents.service'
import type { CV } from '../../../types/documents'

export function useCVs() {
  const [cvs, setCVs] = useState<CV[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchCVs = useCallback(async () => {
    setLoading(true)
    setError(null)
    try {
      const data = await documentsService.listCVs()
      setCVs(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load CVs')
    } finally {
      setLoading(false)
    }
  }, [])

  return { cvs, loading, error, fetchCVs }
}
