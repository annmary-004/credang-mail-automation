import axios from 'axios'

const API = axios.create({ baseURL: '/api' })

API.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

export default API

// ── Auth helpers ─────────────────────────────────────────────────────────────
export function useAuth() {
  const token = localStorage.getItem('token')
  const name  = localStorage.getItem('name')
  const email = localStorage.getItem('email')
  return { token, name, email }
}

export function saveAuth({ access_token, name, email }) {
  localStorage.setItem('token', access_token)
  localStorage.setItem('name',  name)
  localStorage.setItem('email', email)
}

export function clearAuth() {
  localStorage.removeItem('token')
  localStorage.removeItem('name')
  localStorage.removeItem('email')
}

