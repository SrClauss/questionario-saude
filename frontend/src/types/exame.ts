export interface Exame {
    id: string;
    avaliacao_id: string;
    paciente_id: string;
    tamanho_pdf: number | null;
    marcado_para_delecao: boolean;
    created_at: string; // ISO string date
    updated_at: string; // ISO string date
}
