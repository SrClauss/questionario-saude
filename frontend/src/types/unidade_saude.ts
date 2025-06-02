
export class UnidadeSaude{

    id: string;
        nome: string;
        cnpj: string;
        endereco: any; // Assuming endereco is a JSON object
        telefone?: string;
        email?: string;
        created_at: string; // Assuming ISO 8601 string
        updated_at: string; // Assuming ISO 8601 string
        avaliacao?: any; // Assuming Avaliacao is a related object
    
        constructor(data: any) {
            this.id = data.id;
            this.nome = data.nome;
            this.cnpj = data.cnpj;
            this.endereco = data.endereco;
            this.telefone = data.telefone;
            this.email = data.email;
            this.created_at = data.created_at;
            this.updated_at = data.updated_at;
            this.avaliacao = data.avaliacao;
        }
        
}

/*

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
    data_inicio = Column(Date, nullable=False)
    unidade_saude_id = Column(String(26), ForeignKey('unidades_saude.id', ondelete='CASCADE')) # Removida vírgula extra
    laudo_id = Column(String(26), ForeignKey('laudos.id', ondelete='CASCADE'), unique=True, nullable=False) # Adicionado unique=True e nullable=False explicitamente
    fechada = Column(Boolean, default=False)


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

    unidade_saude = relationship("UnidadeSaude", back_populates="avaliacao")

    def __repr__(self):
            return f"<Avaliacao(id='{self.id}', data_inicio='{self.data_inicio}')>"
    

    def to_json(self):
        return {
            'id': self.id,
            'data_inicio': self.data_inicio.isoformat(),
            'CIDS': self.CIDS,
            'laudo1': self.laudo1,
            'laudo2': self.laudo2,
            'consideracoes_gerais': self.consideracoes_gerais,
            'abordagem_terapeutica1': self.abordagem_terapeutica1,
            'abordagem_tetrapeutica2': self.abordagem_tetrapeutica2,
            'fechada': self.fechada,
            'baterias_testes': [bateria.to_json() for bateria in self.baterias_testes],
            'laudo': self.laudo.to_json() if self.laudo else None
        }
        
class Laudo(db.Model):
    
    __tablename__ = 'laudos'
    
    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    medico_id = Column(String(26), ForeignKey('medicos.id', ondelete='CASCADE'))
    paciente_id = Column(String(26), ForeignKey('pacientes.id', ondelete='CASCADE'))
    cid = Column(String(10), nullable=False)
    data = Column(Date, nullable=False)
    parecer = Column(Text, nullable=False)
    abordagem_terapeutica = Column(Text, nullable=False)
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
 
 */