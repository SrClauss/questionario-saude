export interface FonteBibliografica {
  titulo: string;
  autores: string;
  ano: string;
  editora?: string; // Editora é opcional
  local?: string; // Local é opcional
}

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
  pergunta_condicional?: PerguntaCondicional; // Campo opcional para a pergunta condicional
  respostas_condicionais?: RespostaCondicional[]; // Campo opcional para as respostas condicionais
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