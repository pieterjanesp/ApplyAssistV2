import { Card } from '../../components/ui/Card'
import { LoadingSpinner } from '../../components/common/LoadingSpinner'
import { useProfile } from './hooks/useProfile'

export function ProfilePage() {
  const { profile, loading, error } = useProfile()

  if (loading) return <LoadingSpinner className="mt-12" />
  if (error) return <p className="text-red-600">{error}</p>

  return (
    <div className="mx-auto max-w-3xl">
      <h1 className="mb-6 text-2xl font-bold text-gray-900">Profile</h1>
      {profile ? (
        <Card>
          <div className="space-y-4">
            <div>
              <span className="text-sm text-gray-500">Name</span>
              <p className="text-gray-900">{profile.full_name}</p>
            </div>
            <div>
              <span className="text-sm text-gray-500">Email</span>
              <p className="text-gray-900">{profile.email}</p>
            </div>
            {profile.location && (
              <div>
                <span className="text-sm text-gray-500">Location</span>
                <p className="text-gray-900">{profile.location}</p>
              </div>
            )}
            {profile.summary && (
              <div>
                <span className="text-sm text-gray-500">Summary</span>
                <p className="text-gray-900">{profile.summary}</p>
              </div>
            )}
            {profile.skills.length > 0 && (
              <div>
                <span className="text-sm text-gray-500">Skills</span>
                <div className="mt-1 flex flex-wrap gap-2">
                  {profile.skills.map((skill) => (
                    <span
                      key={skill}
                      className="rounded-full bg-blue-50 px-3 py-1 text-sm text-blue-700"
                    >
                      {skill}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </Card>
      ) : (
        <Card>
          <p className="text-gray-600">No profile yet. Create one to get started.</p>
        </Card>
      )}
    </div>
  )
}
