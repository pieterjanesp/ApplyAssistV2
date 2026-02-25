import { Navigate, Outlet } from 'react-router-dom'
import { useAuthStore } from '../../store/authStore'
import { ROUTES } from '../../config/routes'

export function ProtectedRoute() {
  const { session, loading } = useAuthStore()

  if (loading) {
    return (
      <div className="flex h-screen items-center justify-center">
        <div className="text-lg text-gray-500">Loading...</div>
      </div>
    )
  }

  if (!session) {
    return <Navigate to={ROUTES.LOGIN} replace />
  }

  return <Outlet />
}
