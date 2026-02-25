import { Routes, Route, Navigate } from 'react-router-dom'
import { ROUTES } from './config/routes'
import { AuthProvider } from './domains/auth/AuthProvider'
import { ProtectedRoute } from './domains/auth/ProtectedRoute'
import { LoginPage } from './domains/auth/LoginPage'
import { ProfilePage } from './domains/profile/ProfilePage'
import { InfoExtractionPage } from './domains/profile/InfoExtractionPage'
import { CVGenerationPage } from './domains/documents/CVGenerationPage'
import { CVOptimisationPage } from './domains/documents/CVOptimisationPage'
import { JobCatalogPage } from './domains/jobs/JobCatalogPage'
import { JobDetailPage } from './domains/jobs/JobDetailPage'
import { JobApplicationPage } from './domains/applications/JobApplicationPage'
import { JobManagerPage } from './domains/applications/JobManagerPage'
import { PageContainer } from './components/layout/PageContainer'

function App() {
  return (
    <AuthProvider>
      <Routes>
        <Route path={ROUTES.LOGIN} element={<LoginPage />} />
        <Route element={<ProtectedRoute />}>
          <Route element={<PageContainer />}>
            <Route path={ROUTES.HOME} element={<Navigate to={ROUTES.PROFILE} replace />} />
            <Route path={ROUTES.PROFILE} element={<ProfilePage />} />
            <Route path={ROUTES.PROFILE_EXTRACTION} element={<InfoExtractionPage />} />
            <Route path={ROUTES.CV_GENERATE} element={<CVGenerationPage />} />
            <Route path={ROUTES.CV_OPTIMISE} element={<CVOptimisationPage />} />
            <Route path={ROUTES.JOBS} element={<JobCatalogPage />} />
            <Route path={ROUTES.JOB_DETAIL} element={<JobDetailPage />} />
            <Route path={ROUTES.APPLICATION_NEW} element={<JobApplicationPage />} />
            <Route path={ROUTES.APPLICATION_MANAGER} element={<JobManagerPage />} />
          </Route>
        </Route>
      </Routes>
    </AuthProvider>
  )
}

export default App
