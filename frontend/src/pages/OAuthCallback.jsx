import { useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { saveAuth } from '../api/auth'

export default function OAuthCallback() {
  const [params] = useSearchParams()
  const navigate = useNavigate()

  useEffect(() => {
    const token = params.get('token')
    const name  = params.get('name')
    const email = params.get('email')
    if (token) {
      saveAuth({ access_token: token, name, email })
      navigate('/', { replace: true })
    } else {
      navigate('/login', { replace: true })
    }
  }, [])

  return <div className="min-h-screen flex items-center justify-center"><p>Signing you in…</p></div>
}

