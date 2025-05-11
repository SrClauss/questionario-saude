import React, { useState, useEffect, useCallback } from 'react';
import {
    Modal,
    Box,
    Typography,
    TextField,
    Button,
    IconButton,
    Divider,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Alert,
} from '@mui/material';
import { AddCircleOutline, RemoveCircleOutline } from '@mui/icons-material';
import RenderAlternativas from '../../components/AlternativaForm';
import { Alternativa } from '../../types/questionario';

export interface PerguntaData {
    id?: string;
    texto: string;
    tipo_resposta: string;
    ordem: number;
    is_obrigatoria: boolean;
    sessao_id: string;
    alternativas: Alternativa[];
    metodo_pontuacao: string;
}

interface PerguntasEmLoteModalProps {
    open: boolean;
    onClose: () => void;
    onSave: (perguntas: PerguntaData[]) => void;
    sessaoId: string;
}

const PerguntasEmLoteModal: React.FC<PerguntasEmLoteModalProps> = ({ open, onClose, onSave, sessaoId }) => {
    const [perguntas, setPerguntas] = useState<PerguntaData[]>([
        {
            texto: '',
            tipo_resposta: 'texto',
            ordem: 1,
            is_obrigatoria: false,
            sessao_id: sessaoId,
            alternativas: [],
            metodo_pontuacao: 'soma_item',
        }
    ]);
    const [globalTipo, setGlobalTipo] = useState<string>('texto');
    const [globalMetodoPontuacao, setGlobalMetodoPontuacao] = useState<string>('soma_item');
    const [alternativas, setAlternativas] = useState<Alternativa[]>([]);
    const [showValidationAlert, setShowValidationAlert] = useState(false);
    const [errors, setErrors] = useState<{ [key: number]: string }>({});

    useEffect(() => {
        setPerguntas(prev => prev.map(p => ({ ...p, tipo_resposta: globalTipo })));
    }, [globalTipo]);

    useEffect(() => {
        setPerguntas(prev => prev.map(p => ({ ...p, metodo_pontuacao: globalMetodoPontuacao })));
    }, [globalMetodoPontuacao]);

    const handleSave = useCallback(() => {
        // Validação simples: texto mínimo de 5 caracteres para cada pergunta
        let valid = true;
        const newErrors: { [key: number]: string } = {};
        perguntas.forEach((p, idx) => {
            if (!p.texto.trim() || p.texto.trim().length < 5) {
                valid = false;
                newErrors[idx] = 'O texto deve ter pelo menos 5 caracteres';
            }
        });
        setErrors(newErrors);
        setShowValidationAlert(!valid);
        if (!valid) return;

        const perguntasComAlternativas = perguntas.map(p => ({
            ...p,
            alternativas: alternativas,
        }));
        onSave(perguntasComAlternativas);
        onClose();
    }, [perguntas, alternativas, onSave, onClose]);

    const handleAddPergunta = () => {
        setPerguntas(prev => [
            ...prev,
            {
                texto: '',
                tipo_resposta: globalTipo,
                ordem: prev.length + 1,
                is_obrigatoria: false,
                sessao_id: sessaoId,
                alternativas: [],
                metodo_pontuacao: globalMetodoPontuacao,
            }
        ]);
    };

    const handleRemovePergunta = (index: number) => {
        if (perguntas.length <= 1) return;
        setPerguntas(prev => prev.filter((_, idx) => idx !== index));
    };

    const handleChangePerguntaTexto = (index: number, newTexto: string) => {
        setPerguntas(prev =>
            prev.map((p, idx) => (idx === index ? { ...p, texto: newTexto } : p))
        );
    };

    const handleSetAlternativas = useCallback((alts: Alternativa[]) => {
        setAlternativas(alts);
    }, []);

    return (
        <Modal open={open} onClose={onClose}>
            <Box
                sx={{
                    backgroundColor: 'white',
                    width: { xs: '90%', sm: '60%', md: '40%' },
                    margin: 'auto',
                    marginTop: '10%',
                    padding: 3,
                    borderRadius: 2,
                    maxHeight: '90vh',
                    overflowY: 'auto',
                }}
            >
                <Typography variant="h6" sx={{ mb: 2 }}>
                    Criar Perguntas em Lote
                </Typography>

                {showValidationAlert && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                        Por favor, corrija os erros no formulário para continuar.
                    </Alert>
                )}

                <FormControl fullWidth margin="normal">
                    <InputLabel id="tipo-global-label">Tipo de Resposta</InputLabel>
                    <Select
                        labelId="tipo-global-label"
                        value={globalTipo}
                        label="Tipo de Resposta"
                        onChange={e => setGlobalTipo(e.target.value)}
                    >
                        <MenuItem value="escala_likert_3">Escala Likert(3 alternativas)</MenuItem>
                        <MenuItem value="escala_likert_4">Escala Likert(4 alternativas)</MenuItem>
                        <MenuItem value="escala_likert_5">Escala Likert(5 alternativas)</MenuItem>
                        <MenuItem value="escala_likert_7">Escala Likert(7 alternativas)</MenuItem>
                        <MenuItem value="texto">Texto</MenuItem>
                        <MenuItem value="booleano">Sim/Não</MenuItem>
                        <MenuItem value="personalizado">Personalizado</MenuItem>
                        <MenuItem value="numero">Número</MenuItem>
                    </Select>
                </FormControl>

                <FormControl fullWidth margin="normal">
                    <InputLabel id="metodo-pontuacao-global-label">Método de Pontuação</InputLabel>
                    <Select
                        labelId="metodo-pontuacao-global-label"
                        value={globalMetodoPontuacao}
                        label="Método de Pontuação"
                        onChange={e => setGlobalMetodoPontuacao(e.target.value)}
                    >
                        <MenuItem value="soma_item">Soma dos Itens</MenuItem>
                        <MenuItem value="qualitativo">Qualitativo</MenuItem>
                        <MenuItem value="moda_itens">Moda</MenuItem>
                        <MenuItem value="media_sessao">Média</MenuItem>
                        <MenuItem value="formula_anterior">Fórmula Anterior</MenuItem>
                    </Select>
                </FormControl>

                {(globalTipo !== 'texto' && globalTipo !== 'numero') && (
                    <RenderAlternativas
                        tipo_resposta={globalTipo}
                        onSetAlternativas={handleSetAlternativas}
                        alternativas={alternativas}
                        pergunta_id=""
                    />
                )}

                <Divider sx={{ my: 2 }} />

                {perguntas.map((p, idx) => (
                    <Box key={idx} sx={{ mb: 2 }}>
                        <TextField
                            label={`Texto da Pergunta ${idx + 1}`}
                            fullWidth
                            value={p.texto}
                            onChange={e => handleChangePerguntaTexto(idx, e.target.value)}
                            margin="normal"
                            error={!!errors[idx]}
                            helperText={errors[idx]}
                        />
                        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                            <IconButton color="error" onClick={() => handleRemovePergunta(idx)}>
                                <RemoveCircleOutline />
                            </IconButton>
                        </Box>
                    </Box>
                ))}

                <Button
                    variant="contained"
                    startIcon={<AddCircleOutline />}
                    onClick={handleAddPergunta}
                    sx={{ mb: 2 }}
                >
                    Adicionar Pergunta
                </Button>

                <Box sx={{ display: 'flex', justifyContent: 'space-around', gap: 1 }}>
                    <Button variant="outlined" fullWidth onClick={onClose}>
                        Cancelar
                    </Button>
                    <Button variant="contained" fullWidth onClick={handleSave}>
                        Salvar
                    </Button>
                </Box>
            </Box>
        </Modal>
    );
};

export default PerguntasEmLoteModal;