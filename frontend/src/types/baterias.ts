/*


class BateriaTestes(db.Model):  # Alterado: Base -> db.Model
    __tablename__ = 'baterias_testes'

    id = Column(String(26), primary_key=True, default=lambda: str(ulid.ULID()))
    profissional_saude_id = Column(String(26), ForeignKey('profissionais_saude.id', ondelete='CASCADE'))
    paciente_id = Column(String(26), ForeignKey('pacientes.id', ondelete='CASCADE'))
    colaborador_id = Column(String(26), ForeignKey('colaboradores.id', ondelete='CASCADE'), nullable=True)
    questionario_id = Column(String(26), ForeignKey('questionarios.id', ondelete='CASCADE'))
    data_aplicacao = Column(Date, nullable=False)
    respostas = Column(JSON, nullable=True)
    observacoes = Column(Text)
    is_completo = Column(Boolean, default=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    # Relacionamentos
    profissional_saude = relationship("ProfissionalSaude", back_populates="baterias_testes")
    paciente = relationship("Paciente", back_populates="baterias_testes")
    colaborador = relationship("Colaborador", back_populates="baterias_testes")
    questionario = relationship("Questionario", back_populates="baterias_testes")

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
            'is_completo': self.is_completo,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

*/
interface Resposta {
    pergunta_id: string;
    alternativa_id: string;
}

export class BateriaTestes {
    id: string;
    profissional_saude_id: string;
    paciente_id: string;
    colaborador_id: string | null;
    questionario_id: string;
    data_aplicacao: Date;
    respostas: Resposta[];
    observacoes: string | null;
    is_completo: boolean;
    created_at: Date;
    updated_at: Date;
    total_perguntas: number; // Campo adicional para armazenar o total de perguntas

    constructor(data: any) {
        this.id = data.id;
        this.profissional_saude_id = data.profissional_saude_id;
        this.paciente_id = data.paciente_id;
        this.colaborador_id = data.colaborador_id || null;
        this.questionario_id = data.questionario_id;
        this.data_aplicacao = new Date(data.data_aplicacao);
        this.respostas = Array.isArray(data.respostas) ? data.respostas : [];
        this.observacoes = data.observacoes || null;
        this.is_completo = data.is_completo || false;
        this.created_at = new Date(data.created_at);
        this.updated_at = new Date(data.updated_at);
        this.total_perguntas = data.total_perguntas || 0; // Inicializa com o valor do backend ou 0 se não existir
    }
    
    // Método auxiliar para calcular progresso
    get progresso(): number {
        if (this.total_perguntas === 0) return 0;
        return (this.respostas.length / this.total_perguntas) * 100;
    }
}
