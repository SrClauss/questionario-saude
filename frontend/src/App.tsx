import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from './providers/ThemeProvider'
import { Route, Routes } from 'react-router-dom'
import LoginScreen from './screens/LoginScreen'
import HomeRouter from './components/HomeRouter'
import PacienteScreen from './screens/PacienteScreen'
import ProfissionalSaudeScreen from './screens/ProfissionalSaudeScreen'
import ColaboradorScreen from './screens/ColaboradorScreen'
import QuestionarioScreen from './screens/QuestionarioScreen'
import CadastroQuestionarioScreen from './screens/CadastroQuestionarioScreen'
import ConfirmPasswordScreen from './screens/ConfirmPasswordScreen'
import TestesAplicadosPacienteScreen from './screens/TestesAplicadosPacienteScreen'
import MedicoScreen from './screens/MedicoScreen'
import UnidadeSaudeScreen from './screens/UnidadeSaudeScreen'
import { UnidadeSaudeProvider } from './contexts/UnidadesSaudeContext'
import AvaliacaoScreen from './screens/AvaliacaoScreen'
import BateriaScreen from './screens/BateriaScreen'
import ConfigScreen from './screens/ConfigScreen'
function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
        <UnidadeSaudeProvider>
          <Routes>
            <Route path="/" element={<HomeRouter />} />
            <Route path="/login" element={<LoginScreen />} />
            <Route path="/unauthorized" element={<div>Unauthorized</div>} />
            <Route path='/paciente' element={<PacienteScreen />} />
            <Route path='/profissional' element={<ProfissionalSaudeScreen />} />
            <Route path='/colaborador' element={<ColaboradorScreen />} />
            <Route path='/questionario' element={<QuestionarioScreen />} />
            <Route path='/cadastro-questionario' element={<CadastroQuestionarioScreen />} />
            <Route path='/cadastro-questionario/:id' element={<CadastroQuestionarioScreen />} />
            <Route path='/confirm-email/:token' element={<ConfirmPasswordScreen />} />
            <Route path='/bateria/:id' element={<BateriaScreen />} />
            <Route path='/paciente-baterias-list' element={<TestesAplicadosPacienteScreen />} />
            <Route path='/medico' element={<MedicoScreen />} />
            <Route path='/unidade-saude' element={<UnidadeSaudeScreen />} />
            <Route path='/avaliacao/:paciente_id' element={<AvaliacaoScreen />} />
            <Route path='/config' element={<ConfigScreen />} />
          </Routes>
        </UnidadeSaudeProvider>
      </ThemeProvider>
    </BrowserRouter>
  )
}

export default App
