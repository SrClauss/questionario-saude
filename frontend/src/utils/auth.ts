import { jwtDecode } from 'jwt-decode'

interface TokenPayload {
  id: string
  email: string
  exp: number
  role: 'admin' | 'profissional' | 'paciente' | 'colaborador'
}

interface User {
  id: string
  email: string
  is_active: boolean
  created_at: string
  updated_at: string
  token: string
}

interface Colaborador {
  id: string
  nome: string
  telefone: string | null
  enderecos: any | null
  funcao: string | null
  created_at: string
  updated_at: string
  user_id: string
}

interface Paciente {
  id: string
  nome: string
  telefone: string | null
  enderecos: any | null
  created_at: string
  updated_at: string
  user_id: string
}

interface ProfissionalSaude {
  id: string
  nome: string
  telefone: string | null
  enderecos: any | null
  registro_profissional: string
  tipo_registro: string
  estado_registro: string
  created_at: string
  updated_at: string
  user_id: string
}

interface AuthResponse {
  user: User
  colaborador: Colaborador | null
  paciente: Paciente | null
  profissional_saude: ProfissionalSaude | null
}

export const TOKEN_KEY = '@App:token'
export const USER_KEY = '@App:user'
export const PROFILE_KEY = '@App:profile'

export const auth = {
  /**
   * Salva os dados no localStorage
   */
  setToken(data: AuthResponse): void {

    console.log('setToken', data)
    // Salva o token
    localStorage.setItem(TOKEN_KEY, data.user.token)
    
    // Salva dados do usuário
    localStorage.setItem(USER_KEY, JSON.stringify(data.user))
    
    // Salva o perfil específico (colaborador, paciente ou profissional)
    const profile = data.colaborador || data.paciente || data.profissional_saude
    if (profile) {
      localStorage.setItem(PROFILE_KEY, JSON.stringify(profile))
    }
  },
  
  /**
   * Recupera o token do localStorage
   */
  getToken(): string | null {
    return localStorage.getItem(TOKEN_KEY)
  },

  /**
   * Recupera os dados do usuário
   */
  getUser(): User | null {
    const user = localStorage.getItem(USER_KEY)
    return user ? JSON.parse(user) : null
  },

  /**
   * Recupera o perfil específico
   */
  getProfile(): Colaborador | Paciente | ProfissionalSaude | null {
    const profile = localStorage.getItem(PROFILE_KEY)
    return profile ? JSON.parse(profile) : null
  },

  /**
   * Remove todos os dados do localStorage
   */
  removeToken(): void {
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(USER_KEY)
    localStorage.removeItem(PROFILE_KEY)
  },

  /**
   * Verifica se o token é válido
   */
  isValidToken(): boolean {
    const token = this.getToken()

    if (!token) {
      return false
    }

    try {
      const decoded = jwtDecode<TokenPayload>(token)
      const currentTime = Date.now() / 1000

      if (decoded.exp < currentTime) {
        this.removeToken()
        return false
      }

      return true
    } catch {
      this.removeToken()
      return false
    }
  },

  /**
   * Obtém os dados do usuário do token
   */
  getUserData(): TokenPayload | null {
    const token = this.getToken()

    if (!token) {
      return null
    }

    try {
      return jwtDecode<TokenPayload>(token)
    } catch {
      return null
    }
  },
}