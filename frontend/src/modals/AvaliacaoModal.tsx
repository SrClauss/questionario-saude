import { Avaliacao, TipoPagamento } from "../types/avaliacao";
import { useEffect, useState, useReducer,  useContext } from 'react'
import { Paciente } from "../types/user";
import {
    Modal,
    Box,
    Typography,
    TextField,
    Button,
    CircularProgress,
    Select,
    MenuItem,
    FormControl,
    InputLabel,
    InputAdornment,
    FormControlLabel,
    Switch,
} from "@mui/material";
import { auth } from "../utils/auth";
import { UnidadeSaudeContext } from "../contexts/UnidadesSaudeContext";

// Estilo para o Box do Modal
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

interface AvaliacaoModalProps {
    paciente: Paciente
    initialAvaliacao?: Avaliacao | null
    open: boolean
    onClose: () => void
}

const initialAvaliacaoData: Avaliacao = {
    id: '',
    data_inicio: new Date().toISOString().split('T')[0],
    unidade_saude_id: '',
    laudo_id: null,
    paciente_id: '',
    fechada: false,
    valor_cobranca: 0,
    pago: false,
    tipo_pagamento: '',
    created_at: '',
    updated_at: '',
};

type AvaliacaoAction =
    | { type: 'SET_FIELD'; field: keyof Avaliacao; payload: any }
    | { type: 'RESET_AVALIACAO'; payload: Avaliacao };

const avaliacaoReducer = (state: Avaliacao, action: AvaliacaoAction): Avaliacao => {
    switch (action.type) {
        case 'SET_FIELD':
            // Se o campo 'pago' for desmarcado, limpa o 'tipo_pagamento'
            if (action.field === 'pago' && !action.payload) {
                return { ...state, pago: false, tipo_pagamento: '' };
            }
            return { ...state, [action.field]: action.payload };
        case 'RESET_AVALIACAO':
            return action.payload;
        default:
            return state;
    }
};


export default function AvaliacaoModal({ paciente, initialAvaliacao, open, onClose }: AvaliacaoModalProps) {
    const [avaliacaoState, dispatch] = useReducer(
        avaliacaoReducer,
        initialAvaliacao || { ...initialAvaliacaoData, paciente_id: paciente.id }
    );
    const unidadesSaude = useContext(UnidadeSaudeContext);
    const [isLoading, setIsLoading] = useState(false);
    const [errors, setErrors] = useState<{ data_inicio?: string; unidade_saude_id?: string }>({});
    const mode = initialAvaliacao ? 'edit' : 'create';

    useEffect(() => {
        if (open) {
            if (initialAvaliacao) {
                dispatch({ type: 'RESET_AVALIACAO', payload: { ...initialAvaliacao, paciente_id: paciente.id } });
            } else {
                dispatch({ type: 'RESET_AVALIACAO', payload: { ...initialAvaliacaoData, paciente_id: paciente.id } });
            }
        }
    }, [initialAvaliacao, paciente.id, open]);

    const validate = (): boolean => {
        const tempErrors: { data_inicio?: string; unidade_saude_id?: string } = {};
        if (!avaliacaoState.data_inicio) {
            tempErrors.data_inicio = "Data de início é obrigatória.";
        }
        if (!avaliacaoState.unidade_saude_id.trim()) {
            tempErrors.unidade_saude_id = "Unidade de saúde é obrigatória.";
        }
        setErrors(tempErrors);
        return Object.keys(tempErrors).length === 0;
    };

    const handleSubmit = async () => {
        if (!validate()) return;

        setIsLoading(true);

        const payload = {
            ...avaliacaoState,
            paciente_id: paciente.id,
        };

        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const url = mode === 'create'
            ? `${backendUrl}/avaliacoes`
            : `${backendUrl}/avaliacoes/${avaliacaoState.id}`;

        const method = mode === 'create' ? 'POST' : 'PUT';
        const token = auth.getToken();

        try {
            const response = await fetch(url, {
                method: method,
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(payload),
            });

            if (response.ok) {
                onClose();
            } else {
                const errorData = await response.json().catch(() => ({ error: `Erro ao ${mode === 'create' ? 'criar' : 'atualizar'} avaliação.` }));
                console.error("Erro API:", errorData.error);
            }
        } catch (error) {
            console.error("Erro de rede:", error);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <Modal open={open} onClose={onClose} aria-labelledby="avaliacao-modal-title">
            <Box sx={style}>

                <Typography id="avaliacao-modal-title" variant="h6" component="h2" gutterBottom>
                    {mode === 'create' ? 'Nova Avaliação para ' : 'Editar Avaliação de '} {paciente.nome}
                </Typography>

                <TextField
                    label="Data de Início"
                    type="date"
                    value={avaliacaoState.data_inicio}
                    onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'data_inicio', payload: e.target.value })}
                    fullWidth
                    margin="normal"
                    InputLabelProps={{ shrink: true }}
                    error={!!errors.data_inicio}
                    helperText={errors.data_inicio}
                    disabled={isLoading}
                />
                <FormControl fullWidth margin="normal" error={!!errors.unidade_saude_id}>
                    <InputLabel>Unidade de Saúde</InputLabel>
                    <Select
                        label="Unidade de Saúde"
                        value={avaliacaoState.unidade_saude_id}
                        onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'unidade_saude_id', payload: e.target.value })}
                        disabled={isLoading}
                    >
                        <MenuItem value="">
                            <em>Selecione uma Unidade de Saúde</em>
                        </MenuItem>
                        {unidadesSaude.unidadesSaude.map((unidade) => (
                            <MenuItem key={unidade.id} value={unidade.id}>
                                {unidade.nome}
                            </MenuItem>
                        ))}
                    </Select>
                </FormControl>

                <TextField
                    label="Valor da Cobrança"
                    type="number"
                    value={avaliacaoState.valor_cobranca || ''}
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
                            checked={avaliacaoState.pago || false}
                            onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'pago', payload: e.target.checked })}
                            disabled={isLoading}
                        />
                    }
                    label="Pago"
                    sx={{ mt: 1, display: 'block' }}
                />

                <FormControl fullWidth margin="normal" disabled={isLoading || !avaliacaoState.pago}>
                    <InputLabel>Tipo de Pagamento</InputLabel>
                    <Select
                        label="Tipo de Pagamento"
                        value={avaliacaoState.tipo_pagamento || ''}
                        onChange={(e) => dispatch({ type: 'SET_FIELD', field: 'tipo_pagamento', payload: e.target.value as TipoPagamento })}
                    >
                        <MenuItem value="">
                            <em>Selecione</em>
                        </MenuItem>
                        <MenuItem value="cartao_credito">Cartão de Crédito</MenuItem>
                        <MenuItem value="debito">Débito</MenuItem>
                        <MenuItem value="pix">PIX</MenuItem>
                        <MenuItem value="dinheiro">Dinheiro</MenuItem>
                    </Select>
                </FormControl>

                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end', gap: 2 }}>
                    <Button onClick={onClose} color="secondary" disabled={isLoading}>
                        Cancelar
                    </Button>
                    <Button onClick={handleSubmit} variant="contained" color="primary" disabled={isLoading}>
                        {isLoading ? <CircularProgress size={24} /> : 'Salvar'}
                    </Button>
                </Box>
            </Box>
        </Modal>
    );
}
