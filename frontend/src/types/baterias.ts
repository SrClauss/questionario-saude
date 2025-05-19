
export class BateriaTestes {
    id: string;
    profissional_saude_id: string;
    paciente_id: string;
    colaborador_id: string | null;
    questionario_id: string;
    data_aplicacao: string;
    respostas: {};
    observacoes: string | null;
    is_completo: boolean;
    created_at: string;
    updated_at: string;
    total_perguntas: number; // Campo adicional para armazenar o total de perguntas

    constructor(data: any) {
        this.id = data.id;
        this.profissional_saude_id = data.profissional_saude_id;
        this.paciente_id = data.paciente_id;
        this.colaborador_id = data.colaborador_id || null;
        this.questionario_id = data.questionario_id;
        this.data_aplicacao =data.data_aplicacao;
        this.respostas = Array.isArray(data.respostas) ? data.respostas : [];
        this.observacoes = data.observacoes || null;
        this.is_completo = data.is_completo || false;
        this.created_at = data.created_at;
        this.updated_at = data.updated_at;
        this.total_perguntas = data.total_perguntas || 0; // Inicializa com o valor do backend ou 0 se não existir
    }
    
    // Método auxiliar para calcular progresso
    get progresso(): number {
        if (this.total_perguntas === 0) return 0;
        return (Object.keys(this.respostas).length / this.total_perguntas) * 100;
    }
}
