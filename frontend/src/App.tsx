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
import AplicacaoQuestionarioPacienteScreen from './screens/AplicacaoQuestionarioPacienteScreen'
import AplicacaoPacienteQuestionario from './screens/AplicacaoPacienteQuestionarioScreen'
import TestesAplicadosPacienteScreen from './screens/TestesAplicadosPacienteScreen'
import PacienteBateriasScreen from './screens/PacienteBateriasScreen'
import BateriaScreen from './screens/BateriaScreen'
function App() {
  return (
    <BrowserRouter>
      <ThemeProvider>
          <Routes>
            <Route path="/" element={<HomeRouter />} />
            <Route path="/login" element={<LoginScreen />} />
            <Route path="/unauthorized" element={<div>Unauthorized</div>} />
            <Route path='/paciente' element ={<PacienteScreen />} />
            <Route path='/profissional' element ={<ProfissionalSaudeScreen />} />
            <Route path='/colaborador' element ={<ColaboradorScreen />} />
            <Route path='/questionario' element ={<QuestionarioScreen />} />
            <Route path='/cadastro-questionario' element ={<CadastroQuestionarioScreen />} />
            <Route path='/cadastro-questionario/:id' element ={<CadastroQuestionarioScreen />} />
            <Route path='/confirm-email/:token' element={<ConfirmPasswordScreen />} />
            <Route path='/aplicacao-questionario/:id' element={<AplicacaoQuestionarioPacienteScreen />} />
            <Route path='/aplicacao-paciente-questionario/:id' element={<AplicacaoPacienteQuestionario />} />
            <Route path='/paciente-baterias-list' element={<TestesAplicadosPacienteScreen />} />
            <Route path='/baterias/paciente/:id' element={<PacienteBateriasScreen />} />
            <Route path='/bateria/:id' element={<BateriaScreen />} />


          </Routes>
      </ThemeProvider>
    </BrowserRouter>
  )
}

export default App
