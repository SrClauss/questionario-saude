import { useEffect, useReducer, useState } from 'react';
import {
    Modal, Box, Typography, TextField, Button, CircularProgress,
    FormControlLabel, Switch, FormControl, InputLabel, Select, MenuItem, InputAdornment
} from '@mui/material';
import { Avaliacao, TipoPagamento } from '../types/avaliacao';
import { auth } from '../utils/auth';

const style = {
    position: 'absolute' as 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    width: { xs: '90%', sm: '70%', md: '500px' },
    bgcolor: 'background.paper',
    boxShadow: 24,
    p: 4,
    borderRadius: 2,
    maxHeight: '90vh',
    overflowY: 'auto'
};

interface PagamentoModalProps {
    open: boolean;
    onClose: (shouldRefresh?: boolean) => void; // Adicionado parâmetro para indicar se deve recarregar
    avaliacao: Avaliacao;
}

// Usaremos apenas um subconjunto dos campos da avaliação para o estado
type PagamentoState = Pick<Avaliacao, 'valor_cobranca' | 'pago' | 'tipo_pagamento'>;

type PagamentoAction =
    | { type: 'SET_FIELD'; field: keyof PagamentoState; payload: any }
    | { type: 'RESET_FORM'; payload: Avaliacao };

const pagamentoReducer = (state: PagamentoState, action: PagamentoAction): PagamentoState => {
    switch (action.type) {
        case 'SET_FIELD':
            if (action.field === 'pago' && !action.payload) {
                return { ...state, pago: false, tipo_pagamento: '' };
            }
            return { ...state, [action.field]: action.payload };
        case 'RESET_FORM':
            return {
                valor_cobranca: action.payload.valor_cobranca,
                pago: action.payload.pago,
                tipo_pagamento: action.payload.tipo_pagamento,
            };
        default:
            return state;
    }
};

export default function PagamentoModal({ open, onClose, avaliacao }: PagamentoModalProps) {
    const [pagamentoState, dispatch] = useReducer(pagamentoReducer, {
        valor_cobranca: 0,
        pago: false,
        tipo_pagamento: ''
    });
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        if (open) {
            dispatch({ type: 'RESET_FORM', payload: avaliacao });
        }
    }, [open, avaliacao]);

    const handleSubmit = async () => {
        setIsLoading(true);
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        // Usaremos a rota unificada de atualização que você concordou ser a melhor abordagem
        const url = `${backendUrl}/avaliacoes/${avaliacao.id}`;
        const token = auth.getToken();

        try {
            const response = await fetch(url, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(pagamentoState),
            });

            if (response.ok) {
                onClose(true); // Fecha o modal e sinaliza para recarregar a lista
            } else {
                const errorData = await response.json().catch(() => ({ error: 'Erro ao registrar pagamento.' }));
                console.error("Erro API:", errorData.error);
            }
        } catch (error) {
            console.error("Erro de rede:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Modal open={open} onClose={() => onClose(false)}>
            <Box sx={style}>
                <Typography variant="h6" component="h2" gutterBottom>
                    Registrar Pagamento da Avaliação
                </Typography>

                <TextField
                    label="Valor da Cobrança"
                    type="number"
                    value={pagamentoState.valor_cobranca || ''}
                    onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'valor_cobranca', payload: e.target.value ? parseFloat(e.target.value) : null })}
                    fullWidth
                    margin="normal"
                    InputProps={{
                        startAdornment: <InputAdornment position="start">R$</InputAdornment>,
                    }}
                    disabled={isLoading}
                />

                <FormControlLabel
                    control={
                        <Switch
                            checked={pagamentoState.pago || false}
                            onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'pago', payload: e.target.checked })}
                            disabled={isLoading}
                        />
                    }
                    label="Pago"
                    sx={{ mt: 1, display: 'block' }}
                />

                <FormControl fullWidth margin="normal" disabled={isLoading || !pagamentoState.pago}>
                    <InputLabel>Tipo de Pagamento</InputLabel>
                    <Select
                        label="Tipo de Pagamento"
                        value={pagamentoState.tipo_pagamento || ''}
                        onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'tipo_pagamento', payload: e.target.value as TipoPagamento })}
                    >
                        <MenuItem value=""><em>Selecione</em></MenuItem>
                        <MenuItem value="cartao_credito">Cartão de Crédito</MenuItem>
                        <MenuItem value="debito">Débito</MenuItem>
                        <MenuItem value="pix">PIX</MenuItem>
                        <MenuItem value="dinheiro">Dinheiro</MenuItem>
                    </Select>
                </FormControl>

                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                    <Button onClick={() => onClose(false)} color="secondary" disabled={isLoading}>
                        Cancelar
                    </Button>
                    <Button onClick={handleSubmit} variant="contained" color="primary" disabled={isLoading}>
                        {isLoading ? <CircularProgress size={24} /> : 'Salvar Pagamento'}
                    </Button>
                </Box>
            </Box>
        </Modal>
    );
}