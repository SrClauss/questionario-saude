import React, { useState, useEffect } from 'react';
import {
    Modal,
    Box,
    Typography,
    Button,
    FormControl,
    InputLabel,
    Select,
    MenuItem,
    Alert,
    Divider,
} from '@mui/material';
import RenderAlternativas from '../../components/AlternativaForm';
import { Alternativa } from '../../types/questionario';

interface AlternativasLoteModalProps {
    open: boolean;
    onClose: () => void;
    onSave: (payload: {
        tipo_resposta: string;
        metodo_pontuacao: string;
        alternativas: Alternativa[];
    }) => void;
    sessaoId: string;
}

const AlternativasLoteModal: React.FC<AlternativasLoteModalProps> = ({ open, onClose, onSave}) => {
    const [globalTipo, setGlobalTipo] = useState<string>('texto');
    const [globalMetodoPontuacao, setGlobalMetodoPontuacao] = useState<string>('soma_item');
    const [alternativas, setAlternativas] = useState<Alternativa[]>([]);
    const [showValidationAlert, setShowValidationAlert] = useState(false);

    useEffect(() => {
        if (open) {
            // Ao abrir o modal, reseta os estados
            setGlobalTipo('texto');
            setGlobalMetodoPontuacao('soma_item');
            setAlternativas([]);
            setShowValidationAlert(false);
        }
    }, [open]);

    const handleSave = () => {
        if (alternativas.length === 0 && (globalTipo !== 'texto' && globalTipo !== 'numero')) {
            setShowValidationAlert(true);
            return;
        }
        // Aqui, além de retornar os dados globais, espera-se que o onSave trate a atualização de todas as perguntas da sessao
        onSave({
            tipo_resposta: globalTipo,
            metodo_pontuacao: globalMetodoPontuacao,
            alternativas,
        });
        onClose();
    };

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
                    Alterar Alternativas para Toda a Sessão
                </Typography>

                {showValidationAlert && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                        Por favor, defina pelo menos uma alternativa.
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
                        onSetAlternativas={setAlternativas}
                        alternativas={alternativas}
                        pergunta_id=""
                    />
                )}

                <Divider sx={{ my: 2 }} />

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

export default AlternativasLoteModal;