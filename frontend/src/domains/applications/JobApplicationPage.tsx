import { useState } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { applicationsService } from '../../services/applications.service'
import { ROUTES } from '../../config/routes'

export function JobApplicationPage() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const jobId = searchParams.get('jobId') ?? ''
  const [notes, setNotes] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleApply = async () => {
    if (!jobId) return
    setLoading(true)
    setError(null)
    try {
      await applicationsService.createApplication({
        job_id: jobId,
        notes: notes || undefined,
      })
      navigate(ROUTES.APPLICATION_MANAGER)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create application')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Apply for Job</h1>
      {!jobId ? (
        <Card>
          <p className="text-gray-600">No job selected. Go to the job catalog to find a job.</p>
        </Card>
      ) : (
        <Card>
          <p className="mb-4 text-sm text-gray-600">
            This will generate an adapted CV and cover letter for the selected job.
          </p>
          <div>
            <label className="block text-sm font-medium text-gray-700">Notes (optional)</label>
            <textarea
              value={notes}
              onChange={(e) => setNotes(e.target.value)}
              rows={4}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
              placeholder="Any additional notes for this application..."
            />
          </div>
          {error && <p className="mt-2 text-sm text-red-600">{error}</p>}
          <Button className="mt-4" onClick={handleApply} disabled={loading}>
            {loading ? 'Submitting...' : 'Submit Application'}
          </Button>
        </Card>
      )}
    </div>
  )
}
