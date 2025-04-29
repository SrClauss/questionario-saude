import { Navigate } from 'react-router-dom'
import { auth } from '../utils/auth'
import AdminHomeScreen from '../screens/AdminHomeScreen'
import ProfissionalHomeScreen from '../screens/ProfissionalHomeScreen'
import PacienteHomeScreen from '../screens/PacienteHomeScreen'
import ColaboradorHomeScreen from '../screens/ColaboradorHomeScreen'

export default function HomeRouter() {
  // Verifica se está autenticado
  if (!auth.isValidToken()) {
    return <Navigate to="/login" replace />
  }
  
  // Obtém os dados do usuário do token
  const userData = auth.getUserData()
  
  // Renderiza a tela apropriada baseada na role
  switch(userData?.role) {
    case 'admin':
      return <AdminHomeScreen />
    case 'profissional':
      return <ProfissionalHomeScreen />
    case 'paciente':
      return <PacienteHomeScreen />
    case 'colaborador':
      return <ColaboradorHomeScreen />
    default:
      return <Navigate to="/unauthorized" replace />
  }
}