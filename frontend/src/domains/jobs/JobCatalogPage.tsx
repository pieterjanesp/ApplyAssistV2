import { useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Card } from '../../components/ui/Card'
import { LoadingSpinner } from '../../components/common/LoadingSpinner'
import { useJobs } from './hooks/useJobs'

export function JobCatalogPage() {
  const { jobs, loading, error, fetchJobs } = useJobs()

  useEffect(() => {
    fetchJobs()
  }, [fetchJobs])

  if (loading) return <LoadingSpinner className="mt-12" />

  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Job Catalog</h1>
      {error && <p className="mb-4 text-red-600">{error}</p>}
      {jobs.length === 0 ? (
        <Card>
          <p className="text-gray-600">No jobs found. Check back later or adjust your search.</p>
        </Card>
      ) : (
        <div className="space-y-4">
          {jobs.map((job) => (
            <Link key={job.id} to={`/jobs/${job.id}`}>
              <Card className="transition hover:shadow-md">
                <div className="flex items-start justify-between">
                  <div>
                    <h2 className="text-lg font-semibold text-gray-900">{job.title}</h2>
                    <p className="text-sm text-gray-600">
                      {job.company} &middot; {job.location}
                    </p>
                  </div>
                  {job.salary_range && (
                    <span className="text-sm text-gray-500">{job.salary_range}</span>
                  )}
                </div>
                <p className="mt-2 line-clamp-2 text-sm text-gray-700">{job.description}</p>
              </Card>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
