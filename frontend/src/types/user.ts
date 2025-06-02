import { Endereco } from "./endereco"
export interface User {
  id: string
  email: string
  role: 'admin' | 'profissional' | 'paciente' | 'colaborador'
  is_active: boolean
  created_at: string
  updated_at: string
  token?: string
  // Relacionamentos opcionais
  profissional_saude?: ProfissionalSaude
  paciente?: {
    id: string
    nome: string
    data_nascimento: string
    telefone?: string
    enderecos?: any
    created_at: string
    updated_at: string
  }
  colaborador?: {
    id: string
    nome: string
    telefone?: string
    enderecos?: any
    funcao?: string
    created_at: string
    updated_at: string
  }
}

export class ProfissionalSaude {
    id: string;
    nome: string;
    registro_profissional: string;
    cpf: string;
    tipo_registro: string;
    estado_registro: string;
    perfil: string[];
    enderecos?: Endereco[];
    telefone?: string;
    created_at: string;
    updated_at: string;
    user_id: string;

    constructor(
        id: string,
        nome: string,
        registro_profissional: string,
        cpf: string,
        tipo_registro: string,
        estado_registro: string,
        perfil: string[],
        created_at: string,
        updated_at: string,
        user_id: string,
        enderecos?: Endereco[],
        telefone?: string,
    ) {
        this.id = id;
        this.nome = nome;
        this.registro_profissional = registro_profissional;
        this.cpf = cpf;
        this.tipo_registro = tipo_registro;
        this.estado_registro = estado_registro;
        this.perfil = perfil;
        this.created_at = created_at;
        this.updated_at = updated_at;
        this.user_id = user_id;
        this.enderecos = enderecos;
        this.telefone = telefone;
    }
  }

export type AuthContextType = {
  user: User | null
  isAuthenticated: boolean
  role: string | null
  setCurrentUser: (user: User) => void
  clearUser: () => void
  hasPermission: (allowedRoles: string[]) => boolean
}


export class Paciente {
  id: string;
  nome: string;
  cpf: string;
  data_nascimento: string;
  telefone?: string;
  enderecos?: Endereco[];
  email: string;
  created_at: string;
  updated_at: string;
  user_id: string;

  constructor(
    id: string,
    nome: string,
    cpf: string,
    data_nascimento: string,
    created_at: string,
    updated_at: string,
    telefone?: string,
    enderecos?: Endereco[],
    email: string = '',
    user_id?: string
  ) {
    this.id = id;
    this.nome = nome;
    this.data_nascimento = data_nascimento;
    this.cpf = cpf;
    this.created_at = created_at;
    this.updated_at = updated_at;
    this.telefone = telefone;
    this.enderecos = enderecos;
    this.email = email || '';
    this.user_id = user_id || '';
  }
}

export class Colaborador {
  id: string;
  nome: string;
  cpf: string;
  telefone: string;
  enderecos: Endereco[];
  funcao: string;
  created_at: string;
  updated_at: string;
  user_id: string;

  constructor(
    id: string,
    nome: string,
    cpf: string,
    telefone: string,
    enderecos: Endereco[],
    funcao: string,
    created_at: string,
    updated_at: string,
    user_id: string,
  ) {
    this.id = id;
    this.nome = nome;
    this.cpf = cpf;
    this.telefone = telefone;
    this.enderecos = enderecos;
    this.funcao = funcao;
    this.created_at = created_at;
    this.updated_at = updated_at;
    this.user_id = user_id;
  }
}

export class Medico {
  id: string;
  user_id: string;
  nome: string;
  crm: string;
  especialidade: string;
  created_at: string;
  updated_at: string;

  constructor(
    id: string,
    user_id: string,
    nome: string,
    crm: string,
    especialidade: string,
    created_at: string,
    updated_at: string,

  ) {
    this.id = id;
    this.user_id = user_id;
    this.nome = nome;
    this.crm = crm;
    this.especialidade = especialidade;
    this.created_at = created_at;
    this.updated_at = updated_at;
  }

}

