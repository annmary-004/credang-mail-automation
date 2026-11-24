import { Routes, Route, Navigate } from 'react-router-dom'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'
import DashboardPage from './pages/DashboardPage'
import OAuthCallback from './pages/OAuthCallback'
import { useAuth } from './api/auth'

export default function App() {
  const { token } = useAuth()
  return (
    <Routes>
      <Route path="/login"          element={<LoginPage />} />
      <Route path="/register"       element={<RegisterPage />} />
      <Route path="/oauth-callback" element={<OAuthCallback />} />
      <Route
        path="/*"
        element={token ? <DashboardPage /> : <Navigate to="/login" replace />}
      />
    </Routes>
  )
}

