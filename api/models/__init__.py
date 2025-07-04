from sqlalchemy import (
    JSON, Column, Integer, String, Text, Float,
    ForeignKey, Date, DateTime, Boolean, func
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta # Adicionado timedelta
import ulid
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
# Removido: from app import create_app # Geralmente não é necessário em models.py
from extensions import db # Assumindo que db está em extensions.py
from dotenv import load_dotenv # Adicionado
import os # Adicionado

load_dotenv() # Adicionado

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=True)
    role= Column(String(20), nullable=False, default='paciente')
    is_active = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc)) # Adicionado onupdate

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
        if self.password_hash is None: # Adicionado para evitar erro se password_hash for None
            return False
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"<User(email='{self.email}')>"

    def to_json(self):
        secret_key = os.getenv('SECRET_KEY')
        token = None
        if self.id and secret_key: # Adicionado verificação de secret_key
            try:
                token = jwt.encode(
                    {
                        'id': self.id,
                        'email': self.email,
                        'exp': datetime.now(timezone.utc) + timedelta(hours=12),
                        'role': self.role,
                    },
                    secret_key,
                    algorithm='HS256'
                )
            except Exception as e:
                # Logar o erro seria uma boa prática aqui
                print(f"Erro ao gerar token JWT para user {self.id}: {e}")
                token = None


        return {
            'id': self.id,
            'email': self.email,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
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
    telefone = Column(String(20), nullable=True) # SQL permite NULL
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
            'perfil': self.perfil, # Adicionado perfil ao to_json
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Paciente(db.Model):
    __tablename__ = 'pacientes'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    nome = Column(String(100), nullable=False, index=True)
    data_nascimento = Column(Date, nullable=False)
    telefone = Column(String(20), nullable=True) # SQL permite NULL
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
    # Adicionado relacionamento com Laudos, se um paciente pode ter múltiplos laudos diretamente
    laudos = relationship("Laudo", back_populates="paciente", cascade="all, delete-orphan")
    exames = relationship("Exame", back_populates="paciente", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Paciente(nome='{self.nome}')>"

    def to_json(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'data_nascimento': self.data_nascimento.isoformat() if self.data_nascimento else None,
            'telefone': self.telefone,
            'cpf': self.cpf,
            'enderecos': self.enderecos,
            'user_id': self.user_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Colaborador(db.Model):
    __tablename__ = 'colaboradores'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    nome = Column(String(100), nullable=False, index=True)
    telefone = Column(String(20), nullable=True) # SQL permite NULL
    cpf = Column(String(11), unique=True, nullable=False)
    enderecos = Column(JSON, nullable=True)
    funcao = Column(String(100), nullable=True) # SQL permite NULL
    user_id = Column(String(26), ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    user = relationship("User", back_populates="colaborador")
    baterias_testes = relationship(
        "BateriaTestes",
        back_populates="colaborador",
        cascade="all, delete-orphan" # Mantido, mas verifique se é o desejado
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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Questionario(db.Model):
    __tablename__ = 'questionarios'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    titulo = Column(String(100), nullable=False, index=True)
    descricao = Column(Text, nullable=True) # SQL permite NULL
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
        back_populates="questionario" # Removido cascade, pois BateriaTestes já tem cascade para Questionario
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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Sessao(db.Model):
    __tablename__ = 'sessoes'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    questionario_id = Column(String(26), ForeignKey('questionarios.id', ondelete='CASCADE'))
    titulo = Column(String(500), nullable=False)
    descricao = Column(Text, nullable=True) # SQL permite NULL
    ordem = Column(Integer, nullable=False)
    regras_visibilidade = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

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
        json_sessao = {
            'id': self.id,
            'questionario_id': self.questionario_id,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'ordem': self.ordem,
            'regras_visibilidade': self.regras_visibilidade,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_perguntas:
            json_sessao['perguntas'] = [pergunta.to_json(include_alternativas=True) for pergunta in self.perguntas] # Adicionado include_alternativas
        return json_sessao


class Pergunta(db.Model):
    __tablename__ = 'perguntas'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    sessao_id = Column(String(26), ForeignKey('sessoes.id', ondelete='CASCADE'))
    texto = Column(Text, nullable=False)
    tipo_resposta = Column(String(50), nullable=False)
    metodo_pontuacao = Column(String(50), nullable=True) # SQL permite NULL
    ordem = Column(Integer, nullable=False)
    is_obrigatoria = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    sessao = relationship("Sessao", back_populates="perguntas")
    alternativas = relationship(
        "Alternativa",
        back_populates="pergunta",
        cascade="all, delete-orphan",
        order_by="Alternativa.ordem"
    )

    def __repr__(self):
        return f"<Pergunta(texto='{self.texto[:50]}...', tipo='{self.tipo_resposta}')>"

    def to_json(self, include_alternativas=False): # Adicionado parâmetro
        data = {
            'id': self.id,
            'sessao_id': self.sessao_id,
            'texto': self.texto,
            'tipo_resposta': self.tipo_resposta,
            'metodo_pontuacao': self.metodo_pontuacao,
            'ordem': self.ordem,
            'is_obrigatoria': self.is_obrigatoria,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_alternativas:
            data['alternativas'] = [alt.to_json() for alt in self.alternativas]
        return data


class Alternativa(db.Model):
    __tablename__ = 'alternativas'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    pergunta_id = Column(String(26), ForeignKey('perguntas.id', ondelete='CASCADE'))
    texto = Column(String(200), nullable=False)
    valor = Column(Float, nullable=False) # No SQL é float, mas no modelo antigo era String. Mantido Float.
    ordem = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class BateriaTestes(db.Model):
    __tablename__ = 'baterias_testes'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    profissional_saude_id = Column(String(26), ForeignKey('profissionais_saude.id', ondelete='CASCADE'), nullable=True) # SQL permite NULL
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
    avaliacao = relationship("Avaliacao", back_populates="baterias_testes")

    def __repr__(self):
        return f"<BateriaTestes(paciente_id='{self.paciente_id}', questionario_id='{self.questionario_id}')>"

    def to_json(self):
        return {
            'id': self.id,
            'profissional_saude_id': self.profissional_saude_id,
            'paciente_id': self.paciente_id,
            'colaborador_id': self.colaborador_id,
            'questionario_id': self.questionario_id,
            'data_aplicacao': self.data_aplicacao.isoformat() if self.data_aplicacao else None,
            'observacoes': self.observacoes,
            'respostas': self.respostas if self.respostas is not None else {}, # Ajustado para retornar {} se None
            'is_completo': self.is_completo,
            'avaliacao_id': self.avaliacao_id, # Adicionado avaliacao_id
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class Medico(db.Model):
    __tablename__ = 'medicos'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    user_id = Column(String(26), ForeignKey('users.id', ondelete='CASCADE'), unique=True)
    nome = Column(String(100), nullable=False, index=True)
    crm = Column(String(20), unique=True, nullable=False)
    especialidade = Column(String(100), nullable=True) # SQL permite NULL
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    user = relationship("User", back_populates="medico")
    avaliacoes = relationship("Avaliacao", back_populates="medico", cascade="all, delete-orphan") # Adicionado cascade
    laudos = relationship("Laudo", back_populates="medico", cascade="all, delete-orphan") # Adicionado relacionamento com Laudos

    def __repr__(self):
        return f"<Medico(nome='{self.nome}', crm='{self.crm}')>" # Corrigido para Medico

    def to_json(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'nome': self.nome,
            'crm': self.crm,
            'especialidade': self.especialidade,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class UnidadeSaude(db.Model):
    __tablename__ = 'unidades_saude'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    nome = Column(String(100), nullable=False)
    cnpj = Column(String(14), unique=True, nullable=False)
    endereco = Column(JSON, nullable=False)
    telefone = Column(String(20), nullable=True) # SQL permite NULL
    email = Column(String(120), nullable=True) # SQL permite NULL
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # O relacionamento 'avaliacao' aqui parece ser um-para-um com UnidadeSaude,
    # mas uma UnidadeSaude geralmente tem MUITAS avaliações.
    # Vou assumir que o relacionamento correto é um-para-muitos de UnidadeSaude para Avaliacao.
    avaliacoes = relationship( # Renomeado de 'avaliacao' para 'avaliacoes'
        "Avaliacao",
        back_populates="unidade_saude"
        # Removido uselist=False e cascade, pois o cascade deve estar em Avaliacao.unidade_saude_id
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
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class Avaliacao(db.Model):
    __tablename__ = 'avaliacoes'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    paciente_id = Column(String(26), ForeignKey('pacientes.id', ondelete='CASCADE'))
    data_inicio = Column(Date, nullable=False)
    unidade_saude_id = Column(String(26), ForeignKey('unidades_saude.id', ondelete='CASCADE'), nullable=True) # SQL: ON DELETE CASCADE, mas pode ser NULL
    medico_id = Column(String(26), ForeignKey('medicos.id', ondelete='CASCADE'), nullable=True) # SQL: ON DELETE CASCADE, mas pode ser NULL
    # laudo_id foi removido daqui e movido para Laudo como avaliacao_id
    fechada = Column(Boolean, default=False, nullable=True) # SQL: DEFAULT NULL (implica nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=False)

    # Relacionamento um-para-um com Laudo (Laudo tem a FK avaliacao_id)
    laudo = relationship(
        "Laudo",
        back_populates="avaliacao",
        uselist=False,
        cascade="all, delete-orphan" # Laudo é dependente da Avaliacao
    )
    baterias_testes = relationship(
        "BateriaTestes",
        back_populates="avaliacao",
        cascade="all, delete-orphan"
    )
    medico = relationship("Medico", back_populates="avaliacoes")
    unidade_saude = relationship("UnidadeSaude", back_populates="avaliacoes") # Corrigido back_populates
    paciente = relationship("Paciente", back_populates="avaliacoes")
    exames = relationship("Exame", back_populates="avaliacao", cascade="all, delete-orphan")


    def __repr__(self):
        return f"<Avaliacao(id='{self.id}', data_inicio='{self.data_inicio}')>"

    def to_json(self):
        return {
            'id': self.id,
            'paciente_id': self.paciente_id,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'unidade_saude_id': self.unidade_saude_id,
            'medico_id': self.medico_id, # Adicionado medico_id
            'fechada': self.fechada,
            # 'laudo_id': self.laudo.id if self.laudo else None, # Se quiser o ID do laudo associado
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# Tabela de associação para Laudo e CID
cid_laudos_table = db.Table('cid_laudos',
    Column('cid', String(26), ForeignKey('cids.cid', ondelete='CASCADE'), primary_key=True),    # Corrigido para 'cid'
    Column('laudo_id', String(26), ForeignKey('laudos.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, default=lambda: datetime.now(timezone.utc))
)

class Laudo(db.Model):
    __tablename__ = 'laudos'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    medico_id = Column(String(26), ForeignKey('medicos.id', ondelete='CASCADE'), nullable=True) # SQL: ON DELETE CASCADE, mas pode ser NULL
    paciente_id = Column(String(26), ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=True) # SQL: ON DELETE CASCADE, mas pode ser NULL
    avaliacao_id = Column(String(26), ForeignKey('avaliacoes.id', ondelete='CASCADE'), unique=True, nullable=False) # Chave para Avaliacao
    data = Column(Date, nullable=False)
    parecer = Column(Text, nullable=True)
    abordagem_terapeutica = Column(Text, nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    medico = relationship("Medico", back_populates="laudos") # Corrigido back_populates
    paciente = relationship("Paciente", back_populates="laudos") # Corrigido back_populates
    avaliacao = relationship(
        "Avaliacao",
        back_populates="laudo",
        uselist=False
        # Removido cascade daqui, pois Avaliacao já tem cascade para Laudo
    )
    cids = relationship("CID", secondary=cid_laudos_table, back_populates="laudos") # Usando a tabela de associação

    def __repr__(self):
        return f"<Laudo(id='{self.id}', avaliacao_id='{self.avaliacao_id}')>" # Atualizado repr

    def to_json(self):
        return {
            'id': self.id,
            'medico_id': self.medico_id,
            'paciente_id': self.paciente_id,
            'avaliacao_id': self.avaliacao_id, # Adicionado avaliacao_id
            'data': self.data.isoformat() if self.data else None,
            'parecer': self.parecer,
            'abordagem_terapeutica': self.abordagem_terapeutica,
            'cids': [cid.to_json() for cid in self.cids], # Adicionado CIDs
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }


class CID(db.Model):
    __tablename__ = 'cids'
    # 'cid' é o nome da coluna no SQL, mas 'id' é mais convencional para PK em SQLAlchemy
    # Se você quiser manter 'cid' como nome do atributo no modelo, tudo bem.
    # Vou usar 'cid_code' como atributo para evitar conflito com o nome da tabela de associação.
    cid = Column('cid', String(26), primary_key=True, index=True) # Nome da coluna no BD é 'cid'
    descricao = Column(String(255), nullable=False)
    unidecode_descricao = Column(String(255), nullable=False, index=True)

    laudos = relationship("Laudo", secondary=cid_laudos_table, back_populates="cids") # Usando a tabela de associação

    def __repr__(self):
        return f"<CID(cid='{self.cid}', descricao='{self.descricao}')>"

    def to_json(self):
        return {
            'cid': self.cid, # Usando o nome do atributo/coluna
            'descricao': self.descricao,
            'unidecode_descricao': self.unidecode_descricao
        }

# Removida a classe CID_Laudo aninhada, pois foi substituída pela tabela de associação cid_laudos_table

class Exame(db.Model):
    __tablename__ = 'exames'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    avaliacao_id = Column(String(26), ForeignKey('avaliacoes.id', ondelete='CASCADE'), nullable=True) # SQL permite NULL
    paciente_id = Column(String(26), ForeignKey('pacientes.id', ondelete='CASCADE'), nullable=True) # SQL permite NULL
    marcado_para_delecao = Column(Boolean, default=False, nullable=True) # SQL permite NULL
    tamanho_pdf = Column(Float, nullable=True) # SQL permite NULL
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    avaliacao = relationship("Avaliacao", back_populates="exames")
    paciente = relationship("Paciente", back_populates="exames")

    def __repr__(self):
        return f"<Exame(id='{self.id}', avaliacao_id='{self.avaliacao_id}')>"

    def to_json(self):
        return {
            'id': self.id,
            'avaliacao_id': self.avaliacao_id,
            'paciente_id': self.paciente_id,
            'marcado_para_delecao': self.marcado_para_delecao,
            'tamanho_pdf': self.tamanho_pdf,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
