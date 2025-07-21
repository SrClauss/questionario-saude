export type TipoPagamento = 'cartao_credito' | 'debito' | 'pix' | 'dinheiro' | '';

export interface Avaliacao {
    id: string;
    data_inicio: string;
    unidade_saude_id: string;
    laudo_id: string | null;
    paciente_id: string;
    fechada: boolean;
    created_at: string;
    updated_at: string;
    // Novos campos de pagamento
    valor_cobranca?: number | null;
    pago?: boolean;
    tipo_pagamento?: TipoPagamento;
}
