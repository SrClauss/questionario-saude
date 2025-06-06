from sqlalchemy import (
    JSON, Column, Integer, String, Text, Float,
    ForeignKey, Date, DateTime, Boolean, func
)
from sqlalchemy.orm import relationship
from datetime import datetime, timedelta, timezone
import ulid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import create_app
from extensions import db
from dotenv import load_dotenv
import os

load_dotenv()
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=True)
    role= Column(String(20), nullable=False, default='paciente')
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    profissional_saude = relationship(
        "ProfissionalSaude",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    paciente = relationship(
        "Paciente",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    colaborador = relationship(
        "Colaborador",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )
    medico = relationship(
        "Medico",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan"
    )


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User(email='{self.email}')>"

    def to_json(self):
       
        secret_key = os.getenv('SECRET_KEY')
        token = jwt.encode(
            {
                'id': self.id,
                'email': self.email,
                'exp': datetime.now(timezone.utc) + timedelta(hours=12),
                'role': self.role,
            },
            secret_key,
            algorithm='HS256'
        ) if self.id else None

        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'role': self.role,  
            'token': token
        }


class ProfissionalSaude(db.Model):  
    __tablename__ = 'profissionais_saude'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    nome = Column(String(100), nullable=False, index=True)
    user_id = Column(String(26), ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    registro_profissional = Column(String(50), unique=True, nullable=False)
    tipo_registro = Column(String(20), nullable=False)
    estado_registro = Column(String(2), nullable=False)
    perfil = Column(JSON, nullable=True)
    cpf = Column(String(11), unique=True, nullable=False)
    enderecos = Column(JSON, nullable=True)
    telefone = Column(String(20))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="profissional_saude")
    baterias_testes = relationship(
        "BateriaTestes",
        back_populates="profissional_saude",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<ProfissionalSaude(nome='{self.nome}', registro='{self.registro_profissional}')>"

    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'user_id': self.user_id,
            'registro_profissional': self.registro_profissional,
            'cpf': self.cpf,
            'tipo_registro': self.tipo_registro,
            'estado_registro': self.estado_registro,
            'enderecos': self.enderecos,
            'telefone': self.telefone,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Paciente(db.Model):  
    __tablename__ = 'pacientes'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    nome = Column(String(100), nullable=False, index=True)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20))
    cpf = Column(String(11), unique=True, nullable=False)
    enderecos = Column(JSON, nullable=True)
    user_id = Column(String(26), ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    user = relationship("User", back_populates="paciente")
    baterias_testes = relationship(
        "BateriaTestes",
        back_populates="paciente",
        cascade="all, delete-orphan"
    )
    avaliacoes = relationship(
        "Avaliacao",
        back_populates="paciente",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Paciente(nome='{self.nome}')>"

    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento.isoformat(),
            'telefone': self.telefone,
            'cpf': self.cpf,
            'enderecos': self.enderecos,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Colaborador(db.Model):
    __tablename__ = 'colaboradores'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    nome = Column(String(100), nullable=False, index=True)
    telefone = Column(String(20))
    cpf = Column(String(11), unique=True, nullable=False)
    enderecos = Column(JSON, nullable=True)
    funcao = Column(String(100))
    user_id = Column(String(26), ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    user = relationship("User", back_populates="colaborador")
    baterias_testes = relationship(
        "BateriaTestes",
        back_populates="colaborador",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Colaborador(nome='{self.nome}')>"

    def to_json(self):
    
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'enderecos': self.enderecos,
            'cpf': self.cpf,
            'funcao': self.funcao,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Questionario(db.Model):
    """
    Modelo que representa um questionário ou teste.

    Atributos:
        id (String): Identificador único do questionário (ULID).
        titulo (String): Título do questionário.
        descricao (Text): Descrição do questionário.
        versao (String): Versão do questionário.
        fontes_literatura (JSON): Fontes de literatura utilizadas para a construção do questionário.
        is_active (Boolean): Indica se o questionário está ativo.
        created_at (DateTime): Timestamp de criação.
        updated_at (DateTime): Timestamp da última atualização.

    Relacionamentos:
        sessoes (list): Lista de sessões que compõem o questionário.
        baterias_testes (list): Lista de baterias de testes que utilizam este questionário.
    """
    __tablename__ = 'questionarios'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    titulo = Column(String(100), nullable=False, index=True)
    descricao = Column(Text)
    versao = Column(String(20), nullable=True)
    fontes_literatura = Column(JSON, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    sessoes = relationship(
        "Sessao",
        back_populates="questionario",
        cascade="all, delete-orphan",
        order_by="Sessao.ordem"
    )
    baterias_testes = relationship(
        "BateriaTestes",
        back_populates="questionario",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Questionario(titulo='{self.titulo}', versao='{self.versao}')>"

    def to_json(self):
        return {
            'id': self.id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'versao': self.versao,
            'fontes_literatura': self.fontes_literatura,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Sessao(db.Model):
    """
    Modelo que representa uma sessão dentro de um questionário.

    Atributos:
        id (String): Identificador único da sessão (ULID).
        questionario_id (String): Chave estrangeira para o questionário ao qual a sessão pertence.
        titulo (String): Título da sessão.
        descricao (Text): Descrição da sessão.
        ordem (Integer): Ordem da sessão dentro do questionário.
        pergunta_condicional (JSON): JSON contendo o id e texto da pergunta condicional.
        respostas_condicionais (JSON): JSON contendo array de IDs e textos de alternativas que ativam esta sessão.
        created_at (DateTime): Timestamp de criação.
        updated_at (DateTime): Timestamp da última atualização.

    Relacionamentos:
        questionario (Questionario): Relação com o questionário ao qual a sessão pertence.
        perguntas (list): Lista de perguntas que compõem a sessão.
    """
    __tablename__ = 'sessoes'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    questionario_id = Column(String(26), ForeignKey('questionarios.id', ondelete='CASCADE'))
    titulo = Column(String(500), nullable=False)
    descricao = Column(Text)
    ordem = Column(Integer, nullable=False)
    # Campos antigos para condicionalidade (serão substituídos ou depreciados)
    # pergunta_condicional = Column(JSON, nullable=True)
    # respostas_condicionais = Column(JSON, nullable=True)

    regras_visibilidade = Column(JSON, nullable=True)
    """
    Estrutura esperada para regras_visibilidade:
    {
        "logica_principal_entre_regras": "AND" | "OR", // Como as regras na lista 'regras' são combinadas
        "regras": [
            {

                "pergunta_alvo_id": "ulid_da_pergunta",
                "respostas_necessarias_ids": ["ulid_da_alternativa_sim"],
                "logica_respostas": "OR" // Se múltiplas respostas, como elas são avaliadas (AND/OR)
            },
            {
                 "perguntas_para_calculo_ids": ["ulid_pergunta_1", "ulid_pergunta_2"], // Pontuação será somada
                "pontuacao_minima_exigida": 10,
                "pontuacao_maxima_exigida": 20
            },
      
            {
                 "roles_permitidos": ["terapeuta", "profissional_saude"] // Lista de roles que podem ver a sessão
            }
            // ... outras regras
        ]
    }
    """
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    questionario = relationship("Questionario", back_populates="sessoes")
    perguntas = relationship(
        "Pergunta",
        back_populates="sessao",
        cascade="all, delete-orphan",
        order_by="Pergunta.ordem"
    )

    def __repr__(self):
        return f"<Sessao(titulo='{self.titulo}', ordem={self.ordem})>"

    def to_json(self, include_perguntas=False):
        """
        Converte a sessão para formato JSON.
        """
        json_sessao = {
            'id': self.id,
            'questionario_id': self.questionario_id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'ordem': self.ordem,
            # 'pergunta_condicional': self.pergunta_condicional, # Campo antigo
            # 'respostas_condicionais': self.respostas_condicionais, # Campo antigo
            'regras_visibilidade': self.regras_visibilidade,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        
        if include_perguntas:
            json_sessao['perguntas'] = [pergunta.to_json() for pergunta in self.perguntas]
        
        return json_sessao


class Pergunta(db.Model):
    """
    Modelo que representa uma pergunta dentro de uma sessão.

    Atributos:
        id (String): Identificador único da pergunta (ULID).
        sessao_id (String): Chave estrangeira para a sessão à qual a pergunta pertence.
        texto (Text): Texto da pergunta.
        tipo_resposta (String): Tipo de resposta esperada ("booleano", "escala", "texto", etc.).
        metodo_pontuacao (String): Método de pontuação (se aplicável).
        ordem (Integer): Ordem da pergunta dentro da sessão.
        is_obrigatoria (Boolean): Indica se a pergunta é obrigatória.
        created_at (DateTime): Timestamp de criação.
        updated_at (DateTime): Timestamp da última atualização.

    Relacionamentos:
        sessao (Sessao): Relação com a sessão à qual a pergunta pertence.
        alternativas (list): Lista de alternativas de resposta para a pergunta.
    """
    __tablename__ = 'perguntas'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    sessao_id = Column(String(26), ForeignKey('sessoes.id', ondelete='CASCADE'))
    texto = Column(Text, nullable=False)
    tipo_resposta = Column(String(50), nullable=False)
    metodo_pontuacao = Column(String(50))
    ordem = Column(Integer, nullable=False)
    is_obrigatoria = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    sessao = relationship("Sessao", back_populates="perguntas")
    alternativas = relationship(
        "Alternativa",
        back_populates="pergunta",
        cascade="all, delete-orphan",
        order_by="Alternativa.ordem"
    )

    def __repr__(self):
        return f"<Pergunta(texto='{self.texto[:50]}...', tipo='{self.tipo_resposta}')>"

    def to_json(self):
        return {
            'id': self.id,
            'sessao_id': self.sessao_id,
            'texto': self.texto,
            'tipo_resposta': self.tipo_resposta,
            'metodo_pontuacao': self.metodo_pontuacao,
            'ordem': self.ordem,
            'is_obrigatoria': self.is_obrigatoria,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Alternativa(db.Model):
    """
    Modelo que representa uma alternativa de resposta para uma pergunta.

    Atributos:
        id (String): Identificador único da alternativa (ULID).
        pergunta_id (String): Chave estrangeira para a pergunta à qual a alternativa pertence.
        texto (String): Texto da alternativa.
        valor (Float): Valor associado à alternativa (para pontuação).
        ordem (Integer): Ordem da alternativa dentro da pergunta.
        created_at (DateTime): Timestamp de criação.
        updated_at (DateTime): Timestamp da última atualização.

    Relacionamentos:
        pergunta (Pergunta): Relação com a pergunta à qual a alternativa pertence.
    """
    __tablename__ = 'alternativas'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    pergunta_id = Column(String(26), ForeignKey('perguntas.id', ondelete='CASCADE'))
    texto = Column(String(200), nullable=False)
    valor = Column(Float, nullable=False)
    ordem = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    pergunta = relationship("Pergunta", back_populates="alternativas")

    def __repr__(self):
        return f"<Alternativa(texto='{self.texto[:20]}...', valor={self.valor})>"

    def to_json(self):
        return {
            'id': self.id,
            'pergunta_id': self.pergunta_id,
            'texto': self.texto,
            'valor': self.valor,
            'ordem': self.ordem,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class BateriaTestes(db.Model):  
    __tablename__ = 'baterias_testes'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    profissional_saude_id = Column(String(26), ForeignKey('profissionais_saude.id', ondelete='CASCADE'))
    paciente_id = Column(String(26), ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=False)
    colaborador_id = Column(String(26), ForeignKey('colaboradores.id', ondelete='CASCADE'), nullable=True)
    questionario_id = Column(String(26), ForeignKey('questionarios.id', ondelete='CASCADE'))
    data_aplicacao = Column(Date, nullable=False)
    respostas = Column(JSON, nullable=True)
    observacoes = Column(Text, nullable=True)
    is_completo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    avaliacao_id = Column(String(26), ForeignKey('avaliacoes.id', ondelete='CASCADE'), nullable=True)
    
    
    profissional_saude = relationship("ProfissionalSaude", back_populates="baterias_testes")
    paciente = relationship("Paciente", back_populates="baterias_testes")
    colaborador = relationship("Colaborador", back_populates="baterias_testes")
    questionario = relationship("Questionario", back_populates="baterias_testes")
    
    avaliacao = relationship(
        "Avaliacao",
        back_populates="baterias_testes"
    )


    def __repr__(self):
        return f"<BateriaTestes(paciente_id='{self.paciente_id}', questionario_id='{self.questionario_id}')>"

    def to_json(self):
        return {
            'id': self.id,
            'profissional_saude_id': self.profissional_saude_id,
            'paciente_id': self.paciente_id,
            'colaborador_id': self.colaborador_id,
            'questionario_id': self.questionario_id,
            'data_aplicacao': self.data_aplicacao.isoformat(),
            'observacoes': self.observacoes,
            'respostas': self.respostas if self.respostas !={} else [],
            'is_completo': self.is_completo,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class Medico(db.Model):
    __tablename__ = 'medicos'
    
    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    user_id = Column(String(26), ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    nome = Column(String(100), nullable=False, index=True)
    crm = Column(String(20), unique=True, nullable=False)
    especialidade = Column(String(100))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    user = relationship("User", back_populates="medico")
    avaliacoes = relationship("Avaliacao", back_populates="medico")

    def __repr__(self):
        return f"<Médico'(nome='{self.nome}', crm='{self.crm}')>"

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nome': self.nome,
            'crm': self.crm,
            'especialidade': self.especialidade,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }


class UnidadeSaude(db.Model):
    __tablename__ = 'unidades_saude'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    endereco = Column(JSON, nullable=False)
    telefone = Column(String(20))
    email = Column(String(120))
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    
    avaliacao = relationship(
        "Avaliacao",
        back_populates="unidade_saude",
        uselist=False,
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<UnidadeSaude(nome='{self.nome}')>"

    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'endereco': self.endereco,
            'cnpj': self.cnpj,
            'telefone': self.telefone,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    paciente_id = Column(String(26), ForeignKey('pacientes.id', ondelete='CASCADE'))
    data_inicio = Column(Date, nullable=False)
    unidade_saude_id = Column(String(26), ForeignKey('unidades_saude.id', ondelete='CASCADE')) # Removida vírgula extra
    medico_id = Column(String(26), ForeignKey('medicos.id', ondelete='CASCADE'), nullable=True)
    laudo_id = Column(String(26), ForeignKey('laudos.id', ondelete='CASCADE'), unique=True, nullable=True) # Adicionado unique=True e nullable=False explicitamente
    fechada = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)


    laudo = relationship(
        "Laudo",
        back_populates="avaliacao",
        uselist=False
    )

    baterias_testes = relationship(   
        "BateriaTestes",
        back_populates="avaliacao", 
        cascade="all, delete-orphan"
    )
    
    medico = relationship("Medico", back_populates="avaliacoes")
    unidade_saude = relationship("UnidadeSaude", back_populates="avaliacao")
    paciente = relationship("Paciente", back_populates="avaliacoes")

    def __repr__(self):
            return f"<Avaliacao(id='{self.id}', data_inicio='{self.data_inicio}')>"
    

    def to_json(self):
      return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'data_inicio': self.data_inicio.isoformat(),
            'unidade_saude_id': self.unidade_saude_id,
            'fechada': self.fechada,
            'laudo_id': self.laudo_id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
            
      }
        
class Laudo(db.Model):
    
    __tablename__ = 'laudos'
    
    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    medico_id = Column(String(26), ForeignKey('medicos.id', ondelete='CASCADE'))
    paciente_id = Column(String(26), ForeignKey('pacientes.id', ondelete='CASCADE'))
    data = Column(Date, nullable=False)
    parecer = Column(Text, nullable=True)
    abordagem_terapeutica = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    medico = relationship("Medico")
    paciente = relationship("Paciente")
    
    avaliacao = relationship(
        "Avaliacao",
        back_populates="laudo", 
        uselist=False,
        cascade="all, delete-orphan"
    )
    cids = relationship("CID", secondary="cid_laudos", back_populates="laudos")

    def __repr__(self):
        return f"<Laudo(id='{self.id}', cid='{self.cid}')>"

    def to_json(self):
        return {
            'id': self.id,
            'medico_id': self.medico_id,
            'paciente_id': self.paciente_id,
            'cid': self.cid,
            'data': self.data.isoformat(),
            'parecer': self.parecer,
            'abordagem_terapeutica': self.abordagem_terapeutica,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
 
 
class CID(db.Model):
    __tablename__ = 'cids'
    cid = Column(String(26), primary_key=True, index=True)
    descricao = Column(String(255), nullable=False)
    unidecode_descricao = Column(String(255), nullable=False, index=True)
    
    laudos = relationship("Laudo", secondary="cid_laudos", back_populates="cids")
    def __repr__(self):
        return f"<CID(cid='{self.cid}', descricao='{self.descricao}')>"

    def to_json(self):
        return {
            'cid': self.cid,
            'descricao': self.descricao,
            'unidecode_descricao': self.unidecode_descricao
        }
    
    class CID_Laudo(db.Model):
        __tablename__ = 'cid_laudos'
        cid = Column(String(26), ForeignKey('cids.cid', ondelete='CASCADE'), primary_key=True)
        laudo_id = Column(String(26), ForeignKey('laudos.id', ondelete='CASCADE'), primary_key=True)
        created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))