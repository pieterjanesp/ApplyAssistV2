import { Card } from '../../components/ui/Card'

export function InfoExtractionPage() {
  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Extract Profile Info</h1>
      <Card>
        <p className="text-gray-600">
          Paste your career details, LinkedIn profile, or resume text below to automatically
          extract your professional information.
        </p>
        <textarea
          className="mt-4 block w-full rounded-md border border-gray-300 px-3 py-2 shadow-sm focus:border-blue-500 focus:ring-1 focus:ring-blue-500 focus:outline-none"
          rows={10}
          placeholder="Paste your career information here..."
        />
        <button
          className="mt-4 rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
          disabled
        >
          Extract Info (Coming Soon)
        </button>
      </Card>
    </div>
  )
}
