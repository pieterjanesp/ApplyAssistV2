import { useCallback, useState } from 'react'
import { jobsService } from '../../../services/jobs.service'
import type { Job, JobSearchParams } from '../../../types/jobs'

export function useJobs() {
  const [jobs, setJobs] = useState<Job[]>([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const fetchJobs = useCallback(async (params?: JobSearchParams) => {
    setLoading(true)
    setError(null)
    try {
      const data = await jobsService.listJobs(params)
      setJobs(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load jobs')
    } finally {
      setLoading(false)
    }
  }, [])

  return { jobs, loading, error, fetchJobs }
}
