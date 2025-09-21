import { createContext, useContext, useEffect, useState } from 'react'
import { api } from '../api/client'

type AuthCtx = {
  isAuthenticated: boolean
  token: string | null
  login: (token: string) => void
  logout: () => void
}
const AuthContext = createContext<AuthCtx | null>(null)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(() => localStorage.getItem('token'))

  useEffect(() => {
    if (token) localStorage.setItem('token', token)
    else localStorage.removeItem('token')
    api.setToken(token)
  }, [token])

  return (
    <AuthContext.Provider
      value={{
        isAuthenticated: !!token,
        token,
        login: (t) => setToken(t),
        logout: () => setToken(null),
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const ctx = useContext(AuthContext)
  if (!ctx) throw new Error('useAuth must be used within AuthProvider')
  return ctx
}