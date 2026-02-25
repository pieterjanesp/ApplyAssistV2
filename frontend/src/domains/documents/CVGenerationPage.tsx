import { useState } from 'react'
import { Card } from '../../components/ui/Card'
import { Button } from '../../components/ui/Button'
import { documentsService } from '../../services/documents.service'
import type { CV } from '../../types/documents'

export function CVGenerationPage() {
  const [jobDescription, setJobDescription] = useState('')
  const [targetRole, setTargetRole] = useState('')
  const [generatedCV, setGeneratedCV] = useState<CV | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleGenerate = async () => {
    setLoading(true)
    setError(null)
    try {
      const cv = await documentsService.generateCV({
        job_description: jobDescription || undefined,
        target_role: targetRole || undefined,
      })
      setGeneratedCV(cv)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to generate CV')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Generate CV</h1>
      <Card>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700">Target Role</label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
              placeholder="e.g. Senior Software Engineer"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700">
              Job Description (optional)
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              rows={6}
              className="mt-1 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
              placeholder="Paste a job description to tailor the CV..."
            />
          </div>
          <Button onClick={handleGenerate} disabled={loading}>
            {loading ? 'Generating...' : 'Generate CV'}
          </Button>
          {error && <p className="text-sm text-red-600">{error}</p>}
        </div>
      </Card>
      {generatedCV && (
        <Card className="mt-6">
          <h2 className="mb-4 text-lg font-semibold">{generatedCV.title}</h2>
          {generatedCV.sections.map((section) => (
            <div key={section.id} className="mb-4">
              <h3 className="font-medium text-gray-900">{section.title}</h3>
              <ul className="mt-1 space-y-1">
                {section.items.map((item) => (
                  <li key={item.id} className="text-sm text-gray-700">
                    {item.content}
                  </li>
                ))}
              </ul>
            </div>
          ))}
        </Card>
      )}
    </div>
  )
}
