import { ReactNode } from 'react'
import { useNavigate } from 'react-router-dom'
import { auth } from '../utils/auth'

interface ProtectedRouteProviderProps {
  children: ReactNode
  allowed: ('admin' | 'profissional' | 'paciente' | 'colaborador')[]
}

export function ProtectedRouteProvider({ children, allowed }: ProtectedRouteProviderProps) {
  const navigate = useNavigate()
  const userData = auth.getUserData()

  // Verifica se tem token válido
  if (!auth.isValidToken()) {
    navigate('/login', { replace: true })
    return null
  }

  // Verifica se o usuário tem role permitida
  if (!userData?.role || !allowed.includes(userData.role)) {
    navigate('/unauthorized', { replace: true })
    return null
  }

  return <>{children}</>
}