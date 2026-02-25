import { Card } from '../../components/ui/Card'

export function CVOptimisationPage() {
  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Optimise CV</h1>
      <Card>
        <p className="text-gray-600">
          Select an existing CV and provide optimization instructions to improve it.
        </p>
        <p className="mt-4 text-sm text-gray-500">
          Select a CV from your list, then describe what you'd like to improve.
        </p>
        <button
          className="mt-4 rounded-md bg-blue-600 px-4 py-2 text-white hover:bg-blue-700 disabled:opacity-50"
          disabled
        >
          Optimise (Coming Soon)
        </button>
      </Card>
    </div>
  )
}
