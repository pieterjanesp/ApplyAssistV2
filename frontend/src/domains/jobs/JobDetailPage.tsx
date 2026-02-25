import { useCallback, useEffect, useState } from 'react'
import { useParams, Link } from 'react-router-dom'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { LoadingSpinner } from '../../components/common/LoadingSpinner'
import { jobsService } from '../../services/jobs.service'
import { ROUTES } from '../../config/routes'
import type { Job } from '../../types/jobs'

export function JobDetailPage() {
  const { jobId } = useParams<{ jobId: string }>()
  const [job, setJob] = useState<Job | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  const fetchJob = useCallback(async (id: string) => {
    try {
      const data = await jobsService.getJob(id)
      setJob(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to load job')
    } finally {
      setLoading(false)
    }
  }, [])

  useEffect(() => {
    if (!jobId) return
    fetchJob(jobId)
  }, [jobId, fetchJob])

  if (loading) return <LoadingSpinner className="mt-12" />
  if (error) return <p className="text-red-600">{error}</p>
  if (!job) return <p className="text-gray-600">Job not found.</p>

  return (
    <div className="mx-auto max-w-3xl">
      <Card>
        <h1 className="text-2xl font-bold text-gray-900">{job.title}</h1>
        <p className="mt-1 text-gray-600">
          {job.company} &middot; {job.location}
        </p>
        {job.salary_range && <p className="mt-1 text-sm text-gray-500">{job.salary_range}</p>}
        <div className="mt-6">
          <h2 className="font-semibold text-gray-900">Description</h2>
          <p className="mt-2 whitespace-pre-wrap text-gray-700">{job.description}</p>
        </div>
        {job.requirements.length > 0 && (
          <div className="mt-6">
            <h2 className="font-semibold text-gray-900">Requirements</h2>
            <ul className="mt-2 list-disc space-y-1 pl-5">
              {job.requirements.map((req, i) => (
                <li key={i} className="text-gray-700">
                  {req}
                </li>
              ))}
            </ul>
          </div>
        )}
        <div className="mt-6">
          <Link to={`${ROUTES.APPLICATION_NEW}?jobId=${job.id}`}>
            <Button>Apply for this Job</Button>
          </Link>
        </div>
      </Card>
    </div>
  )
}
