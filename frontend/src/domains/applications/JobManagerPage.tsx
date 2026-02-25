import { useEffect } from 'react'
import { Card } from '../../components/ui/Card'
import { LoadingSpinner } from '../../components/common/LoadingSpinner'
import { useApplications } from './hooks/useApplications'

const statusColors: Record<string, string> = {
  draft: 'bg-gray-100 text-gray-700',
  applied: 'bg-blue-100 text-blue-700',
  interviewing: 'bg-yellow-100 text-yellow-700',
  offered: 'bg-green-100 text-green-700',
  rejected: 'bg-red-100 text-red-700',
  withdrawn: 'bg-gray-100 text-gray-500',
}

export function JobManagerPage() {
  const { applications, loading, error, fetchApplications } = useApplications()

  useEffect(() => {
    fetchApplications()
  }, [fetchApplications])

  if (loading) return <LoadingSpinner className="mt-12" />

  return (
    <div className="mx-auto max-w-4xl">
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Applications</h1>
      {error && <p className="mb-4 text-red-600">{error}</p>}
      {applications.length === 0 ? (
        <Card>
          <p className="text-gray-600">No applications yet. Apply for a job to get started.</p>
        </Card>
      ) : (
        <div className="space-y-4">
          {applications.map((app) => (
            <Card key={app.id}>
              <div className="flex items-center justify-between">
                <div>
                  <p className="font-medium text-gray-900">Job: {app.job_id}</p>
                  {app.notes && <p className="mt-1 text-sm text-gray-600">{app.notes}</p>}
                </div>
                <span
                  className={`rounded-full px-3 py-1 text-xs font-medium ${statusColors[app.status] ?? ''}`}
                >
                  {app.status}
                </span>
              </div>
            </Card>
          ))}
        </div>
      )}
    </div>
  )
}
