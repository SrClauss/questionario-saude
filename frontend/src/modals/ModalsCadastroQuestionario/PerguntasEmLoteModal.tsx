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
    Accordion,
    AccordionSummary,
    AccordionDetails
} from '@mui/material';
import { AddCircleOutline, RemoveCircleOutline, ExpandMore as ExpandMoreIcon } from '@mui/icons-material';
import RenderAlternativas from '../../components/AlternativaForm';
import { Alternativa } from '../../types/questionario';

export interface PerguntaData {
    texto: string;
    tipo_resposta: string;
    ordem: number;
    is_obrigatoria: boolean;
    sessao_id: string;
    alternativas: Alternativa[];
    metodo_pontuacao: string; // Adicionado o campo metodo_pontuacao
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
            metodo_pontuacao: 'soma_item' // Valor padrão
        }
    ]);
    const [globalTipo, setGlobalTipo] = useState<string>('texto');
    const [globalMetodoPontuacao, setGlobalMetodoPontuacao] = useState<string>('soma_item'); // Novo estado
    const [alternativas, setAlternativas] = useState<Alternativa[]>([]);

    useEffect(() => {
        setPerguntas(prevPerguntas => {
            const updated = prevPerguntas.map(p => ({ ...p, tipo_resposta: globalTipo }));
            return updated;
        });
    }, [globalTipo]);

    // Efeito para atualizar o método de pontuação em todas as perguntas
    useEffect(() => {
        setPerguntas(prevPerguntas => {
            const updated = prevPerguntas.map(p => ({ ...p, metodo_pontuacao: globalMetodoPontuacao }));
            return updated;
        });
    }, [globalMetodoPontuacao]);

    const handleSave = useCallback(() => {
        // Atualiza todas as perguntas com as alternativas comuns
        const perguntasComAlternativas = perguntas.map(pergunta => ({
            ...pergunta,
            alternativas: alternativas
        }));
        
        // Payload formatado corretamente
        const payload = {
            perguntas: perguntasComAlternativas.map(pergunta => ({
                texto: pergunta.texto,
                tipo_resposta: pergunta.tipo_resposta,
                ordem: pergunta.ordem,
                is_obrigatoria: pergunta.is_obrigatoria,
                metodo_pontuacao: pergunta.metodo_pontuacao, // Incluir método de pontuação
                alternativas: alternativas.map(alt => ({
                    texto: alt.texto,
                    valor: alt.valor,
                    ordem: alt.ordem
                }))
            }))
        };

        console.log("Payload para salvar:", payload);
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
                metodo_pontuacao: globalMetodoPontuacao // Usar o método global
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

    const handleSetAlternativas = useCallback((newAlternativas: Alternativa[]) => {
        setAlternativas(newAlternativas);
    }, []);

    return (
        <Modal open={open} onClose={onClose}>
            <Box
                sx={{
                    backgroundColor: 'white',
                    width: { xs: '100%', sm: '80%', md: '60%' },
                    height: { xs: '100%', md: 'auto' },
                    maxHeight: { xs: '100vh', md: '80vh' },
                    margin: { xs: 0, sm: 'auto' },
                    mt: { xs: 0, sm: 4 },
                    p: 3,
                    borderRadius: { xs: 0, md: 2 },
                    overflowY: 'auto'
                }}
            >
                <Typography variant="h6" sx={{ mb: 2 }}>
                    Criar Perguntas em Lote
                </Typography>

                <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel id="tipo-global-label">Tipo de Resposta</InputLabel>
                    <Select
                        labelId="tipo-global-label"
                        value={globalTipo}
                        label="Tipo de Resposta"
                        onChange={e => setGlobalTipo(e.target.value)}
                    >
                        <MenuItem value="texto">Texto</MenuItem>
                        <MenuItem value="booleano">Booleano</MenuItem>
                        <MenuItem value="numero">Número</MenuItem>
                        <MenuItem value="escala_likert">Escala Likert 5</MenuItem>
                        <MenuItem value="escala_likert_7">Escala Likert 7</MenuItem>
                        <MenuItem value="personalizado">Personalizado</MenuItem>
                    </Select>
                </FormControl>

                {/* Novo campo para método de pontuação global */}
                <FormControl fullWidth sx={{ mb: 2 }}>
                    <InputLabel id="metodo-pontuacao-global-label">Método de Pontuação</InputLabel>
                    <Select
                        labelId="metodo-pontuacao-global-label"
                        value={globalMetodoPontuacao}
                        label="Método de Pontuação"
                        onChange={e => setGlobalMetodoPontuacao(e.target.value)}
                    >
                        <MenuItem value="soma_item">Soma dos Itens</MenuItem>
                        <MenuItem value="qualitativo">Qualitativo</MenuItem>
                        <MenuItem value="moda">Moda</MenuItem>
                        <MenuItem value="media">Média</MenuItem>
                        <MenuItem value="formula_anterior">Fórmula Anterior</MenuItem>
                    </Select>
                </FormControl>

                <Divider sx={{ mb: 2 }} />

                {(globalTipo === 'escala_likert' ||
                    globalTipo === 'escala_likert_7' ||
                    globalTipo === 'booleano' ||
                    globalTipo === 'personalizado') && (
                    <Box sx={{ mb: 2 }}>
                        <Accordion defaultExpanded>
                            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
                                <Typography>Alternativas Comuns</Typography>
                            </AccordionSummary>
                            <AccordionDetails>
                                <RenderAlternativas
                                    tipo_resposta={globalTipo}
                                    onSetAlternativas={handleSetAlternativas}
                                    alternativas={alternativas}
                                    pergunta_id=''
                                />
                            </AccordionDetails>
                        </Accordion>
                    </Box>
                )}

                {perguntas.map((pergunta, idx) => (
                    <Box
                        key={idx}
                        sx={{
                            display: 'flex',
                            alignItems: 'center',
                            gap: 2,
                            mb: 2,
                            p: 2,
                            border: '1px solid #e0e0e0',
                            borderRadius: 1
                        }}
                    >
                        <TextField
                            label={`Texto da Pergunta ${idx + 1}`}
                            value={pergunta.texto}
                            onChange={e => handleChangePerguntaTexto(idx, e.target.value)}
                            fullWidth
                        />
                        <IconButton color="error" onClick={() => handleRemovePergunta(idx)}>
                            <RemoveCircleOutline />
                        </IconButton>
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

                <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                    <Button variant="outlined" onClick={onClose} fullWidth>
                        Cancelar
                    </Button>
                    <Button variant="contained" onClick={handleSave} fullWidth>
                        Salvar
                    </Button>
                </Box>
            </Box>
        </Modal>
    );
};

export default PerguntasEmLoteModal;