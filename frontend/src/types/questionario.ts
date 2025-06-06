export interface FonteBibliografica {
  titulo: string;
  autores: string;
  ano: string;
  editora?: string; // Editora é opcional
  local?: string; // Local é opcional
}

export interface FaixaDePontuacaoInterface {
  tipo_regra: "FAIXA_DE_PONTUACAO";
  perguntas_para_calculo_ids: string[];
  pontuacao_minima_exigida: number;
  pontuacao_maxima_exigida: number;
}

export interface RespostasEspecificasInterface {
  tipo_regra: "RESPOSTA_ESPECIFICA";
  pergunta_alvo_id: string;
  respostas_necessarias_ids: string[];
  logica_respostas: "AND" | "OR";
}
export interface RoleDoUsuarioInterface {
  tipo_regra: "ROLE_USUARIO";
  roles_permitidos: string[];
}
export type RegrasVisibilidadeType = RespostasEspecificasInterface | FaixaDePontuacaoInterface | RoleDoUsuarioInterface;


export interface Alternativa {
  id?: string;
  pergunta_id: string;
  texto: string;
  valor: number;
  ordem: number;
  created_at?: string;
  updated_at?: string;
}

// Nova interface para a pergunta condicional
export interface PerguntaCondicional {
  id: string;
  texto: string;
}

// Nova interface para as respostas condicionais
export interface RespostaCondicional {
  id: string;
  texto: string;
}

export interface Pergunta {
  id: string;
  sessao_id: string;
  texto: string;
  tipo_resposta: string;
  metodo_pontuacao?: string;
  ordem: number;
  is_obrigatoria: boolean;
  created_at: string;
  updated_at: string;
  alternativas: Alternativa[];
}

export interface Sessao {
  id: string;
  questionario_id: string;
  titulo: string;
  descricao?: string;
  ordem: number;
  regras_visibilidade?: RegrasVisibilidadeType[];
  logica_principal_entre_regras?: "AND" | "OR";
  created_at: string;
  updated_at: string;
  perguntas: Pergunta[];
}

export interface Questionario {
  id: string;
  titulo: string;
  descricao?: string;
  versao?: string;
  fontes_literatura?: FonteBibliografica[];
  is_active: boolean;
  created_at: string;
  updated_at: string;
  sessoes: Sessao[];
}