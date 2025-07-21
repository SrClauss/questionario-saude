import { BrowserRouter } from 'react-router-dom'
import { ThemeProvider } from './providers/ThemeProvider'
import { Route, Routes } from 'react-router-dom'

// Layouts e Rotas
import ProtectedLayout from './layouts/ProtectedLayout'
import HomeRouter from './components/HomeRouter'

// Telas Públicas
import LoginScreen from './screens/LoginScreen'
import ConfirmPasswordScreen from './screens/ConfirmPasswordScreen'
import VerificarAssinaturaScreen from './screens/VerificarAssinaturaScreen'

// Telas Protegidas
import PacienteScreen from './screens/PacienteScreen'
import ProfissionalSaudeScreen from './screens/ProfissionalSaudeScreen'
import ColaboradorScreen from './screens/ColaboradorScreen'
import QuestionarioScreen from './screens/QuestionarioScreen'
import CadastroQuestionarioScreen from './screens/CadastroQuestionarioScreen'
import TestesAplicadosPacienteScreen from './screens/TestesAplicadosPacienteScreen'
import MedicoScreen from './screens/MedicoScreen'
import UnidadeSaudeScreen from './screens/UnidadeSaudeScreen'
import AvaliacaoScreen from './screens/AvaliacaoScreen'
import BateriaScreen from './screens/BateriaScreen'
import ConfigScreen from './screens/ConfigScreen'
import AvaliacaoPacienteScreen from './screens/AvaliacaoPacienteScreen'
import EstatisticasScreen from './screens/EstatisticasScreen'
import PesquisaAvaliacoesMedicoScreen from './screens/PesquisaAvaliacoesMedicoScreen'

function App() {
  return (
    <BrowserRouter basename="/app/">
      <ThemeProvider>
        <Routes>
          {/* Rotas Públicas */}
          <Route path="/login" element={<LoginScreen />} />
          <Route path="/unauthorized" element={<div>Unauthorized</div>} />
          <Route path='/confirm-email/:token' element={<ConfirmPasswordScreen />} />
          <Route path='/verificar-assinatura/:dados_criptografados' element={<VerificarAssinaturaScreen />} />

          {/* Rotas Protegidas */}
          <Route element={<ProtectedLayout />}>
            <Route path="/" element={<HomeRouter />} />
            <Route path='/paciente' element={<PacienteScreen />} />
            <Route path='/profissional' element={<ProfissionalSaudeScreen />} />
            <Route path='/colaborador' element={<ColaboradorScreen />} />
            <Route path='/questionario' element={<QuestionarioScreen />} />
            <Route path='/cadastro-questionario' element={<CadastroQuestionarioScreen />} />
            <Route path='/cadastro-questionario/:id' element={<CadastroQuestionarioScreen />} />
            <Route path='/bateria/:id' element={<BateriaScreen />} />
            <Route path='/paciente-baterias-list/:avaliacao_id' element={<TestesAplicadosPacienteScreen />} />
            <Route path='/medico' element={<MedicoScreen />} />
            <Route path='/unidade-saude' element={<UnidadeSaudeScreen />} />
            <Route path='/avaliacao/:paciente_id' element={<AvaliacaoScreen />} />
            <Route path='/config' element={<ConfigScreen />} />
            <Route path='/avaliacao-paciente' element={<AvaliacaoPacienteScreen />} />
            <Route path='/estatisticas/:id' element={<EstatisticasScreen />} />
            <Route path='/pesquisa-avaliacoes-medico' element={<PesquisaAvaliacoesMedicoScreen />} />
          </Route>
        </Routes>
      </ThemeProvider>
    </BrowserRouter>
  )
}

export default App
