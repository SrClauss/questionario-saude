import { Navigate, Outlet } from "react-router-dom";
import { auth } from "../utils/auth";
import { UnidadeSaudeProvider } from "../contexts/UnidadesSaudeContext";

/**
 * Este componente de layout serve como um portão de segurança para as rotas autenticadas.
 * 1. Ele verifica se existe um token de autenticação válido.
 * 2. Se não houver, redireciona o usuário para a página de login.
 * 3. Se houver, ele renderiza o `UnidadeSaudeProvider` e, em seguida, a rota filha (`<Outlet />`).
 *
 * Isso garante que o contexto `UnidadeSaudeContext` e sua chamada de API associada
 * só sejam executados quando o usuário já estiver logado.
 */
export default function ProtectedLayout() {
  if (!auth.isValidToken()) {
    return <Navigate to="/login" replace />;
  }

  return (
    <UnidadeSaudeProvider>
      <Outlet />
    </UnidadeSaudeProvider>
  );
}