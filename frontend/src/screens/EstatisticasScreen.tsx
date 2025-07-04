// EstatisticasScreen.tsx
import { useParams } from "react-router-dom"
import MedicoLayout from "../layouts/MedicoLayout"
import { useEffect, useState } from "react"
import {
    Accordion, AccordionDetails, AccordionSummary, Box, Button, Card, CardContent,
    Chip, CircularProgress, Divider, Paper, Typography, useTheme, Stack, useMediaQuery,
    IconButton, Tooltip, Snackbar, Alert
} from "@mui/material";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import BarChartIcon from '@mui/icons-material/BarChart';
import DownloadIcon from '@mui/icons-material/Download'; // Importar o ícone de download
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip as RechartsTooltip,
    Legend, ResponsiveContainer, PieChart, Pie, Cell
} from 'recharts';
import LaudoCadastroModal from "../modals/LaudosModal";
import { LaudoFormData } from "../modals/LaudosModal";
import LaudoPDFViewer from "../components/LaudoPdf"; // Importação do componente PDF
import { Medico, Paciente } from "../types/user";

// Interfaces para tipar o payload da API
interface AlternativaDisponivel {
    alternativa_id: string;
    texto: string;
    valor: number | null;
}

interface EstatisticaAlternativaPergunta {
    alternativa_id: string;
    alternativa_texto: string;
    valor: number | null;
    contagem_absoluta: number;
    contagem_relativa_percentual: number;
}

interface PerguntaComResposta {
    pergunta_id: string;
    pergunta_texto: string;
    tipo_resposta: string;
    resposta_id: string | null;
    resposta_texto: string | null;
    resposta_valor_escolhido: number | null;
    alternativas_disponiveis: AlternativaDisponivel[];
    pontuacao_maxima_possivel_pergunta?: number;
    estatisticas_alternativas_pergunta?: EstatisticaAlternativaPergunta[];
}

interface EstatisticasSessao {
    total_pontuacao_obtida: number;
    total_pontuacao_maxima_possivel: number;
    media_pontuacao_obtida_por_pergunta_respondida: number;
    moda_pontuacao_obtida_nas_perguntas: number[];
    percentual_aproveitamento: number;
}

interface SessaoDetalhada {
    id: string;
    titulo: string;
    is_plotavel: boolean;
    perguntas_com_respostas: PerguntaComResposta[];
    estatisticas_sessao?: EstatisticasSessao;
}

interface BateriaDetalhada {
    questionario: any;
    id: string;
    questionario_titulo: string;
    data_aplicacao: string | null;
    sessoes_detalhadas: SessaoDetalhada[];
}

interface PayloadEstatisticas {
    fechada: boolean;
    avaliacao_id: string;
    paciente_nome: string;
    paciente_id: string; // Essencial para o laudo
    paciente_data_nascimento?: string; // Opcional, para preencher Paciente
    paciente_cpf?: string;             // Opcional, para preencher Paciente
    data_avaliacao: string | null;
    perfil_de_saude_detalhado: BateriaDetalhada | null;
    outras_baterias: BateriaDetalhada[];
    paciente: Paciente | null; // Objeto Paciente completo
    medico: Medico | null;     // Objeto Medico completo (o médico que fez a avaliação)
}

const COLORS_PIE = ['#0088FE', '#FFBB28'];
const COLORS_BAR = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2'];

const formatDate = (dateString: string | null | undefined) => {
    if (!dateString) return 'N/A';
    try {
        const date = new Date(dateString + 'T00:00:00'); // Adiciona T00:00:00 para evitar problemas de fuso horário
        return date.toLocaleDateString('pt-BR');
    } catch {
        return 'Data inválida';
    }
};

const getModaLabel = (moda: number[]) => {
    if (moda.length === 0) return 'N/A';
    if (moda.length === 1) return moda[0].toString();
    return `${moda[0]} (e ${moda.length - 1} outros)`;
};

export default function EstatisticasScreen() {
    const [estatisticas, setEstatisticas] = useState<PayloadEstatisticas | null>(null);
    const [expandedSessoes, setExpandedSessoes] = useState<{ [key: string]: boolean }>({});
    const [expandedBaterias, setExpandedBaterias] = useState<{ [key: string]: boolean }>({});
    const [loading, setLoading] = useState(true);
    const theme = useTheme();
    const [hasExames, setHasExames] = useState<boolean | null>(null);
    const avaliacaoId = useParams().id;
    const isMobile = useMediaQuery(theme.breakpoints.down('sm'));

    const [isLaudoModalOpen, setIsLaudoModalOpen] = useState(false);
    const [laudoStatus, setLaudoStatus] = useState<{ message: string, type: 'success' | 'error' | 'info' } | null>(null);
    const [showPdfViewer, setShowPdfViewer] = useState<boolean>(false);

    const fetchEstatisticas = async () => {
        setLoading(true);
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/avaliacoes/estatisticas/${avaliacaoId}`;

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();
            setEstatisticas(data);
        } catch (error) {
            console.error('Error fetching estatísticas:', error);
            setEstatisticas(null);
        } finally {
            setLoading(false);
        }
    };

    const checkHasExames = async (currentAvaliacaoId: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/exames/has_exames/${currentAvaliacaoId}`;

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
            });
            if (response.ok) {
                const data = await response.json();
                setHasExames(data.has_exames);
            } else {
                setHasExames(false);
            }
        } catch (error) {
            console.error('Error checking for exames:', error);
            setHasExames(false);
        }
    };

    useEffect(() => {
        if (avaliacaoId) {
            fetchEstatisticas();
            checkHasExames(avaliacaoId);
        }
    }, [avaliacaoId]);

    const handleDownloadAllExames = async () => {
        if (!avaliacaoId) {
            console.error("ID da avaliação não encontrado para download.");
            return;
        }
        setLoading(true);
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');
        const url = `${baseUrl}/exames/dowload/all/${avaliacaoId}`;

        try {
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ message: "Erro ao baixar os exames." }));
                throw new Error(errorData.message || `Erro ${response.status}: ${response.statusText}`);
            }

            const blob = await response.blob();
            const contentDisposition = response.headers.get('content-disposition');
            let filename = `exames_avaliacao_${avaliacaoId}.zip`;
            if (contentDisposition) {
                const filenameMatch = contentDisposition.match(/filename="?(.+)"?/i);
                if (filenameMatch && filenameMatch.length === 2)
                    filename = filenameMatch[1];
            }

            const downloadUrl = window.URL.createObjectURL(blob);
            const link = document.createElement('a');
            link.href = downloadUrl;
            link.setAttribute('download', filename);
            document.body.appendChild(link);
            link.click();
            link.remove();
            window.URL.revokeObjectURL(downloadUrl);

        } catch (error) {
            console.error('Erro ao baixar os exames:', error);
            alert(`Erro ao baixar exames: ${error instanceof Error ? error.message : String(error)}`);
        } finally {
            setLoading(false);
        }
    };

    const handleOpenLaudoModal = () => {
        if (!estatisticas?.paciente) {
            setLaudoStatus({ message: 'Informações do paciente não carregadas para criar o laudo.', type: 'error' });
            return;
        }
        if (!estatisticas?.medico) {
            setLaudoStatus({ message: 'Informações do médico (da avaliação) não encontradas.', type: 'error' });
            return;
        }
        setLaudoStatus(null);
        setIsLaudoModalOpen(true);
    };

    const handleCloseLaudoModal = () => {
        setIsLaudoModalOpen(false);
    };

    const handleSubmitLaudo = async (laudoDataDoModal: LaudoFormData) => {
        if (!avaliacaoId) {
            setLaudoStatus({ message: 'ID da avaliação não encontrado.', type: 'error' });
            return;
        }
        if (!estatisticas?.medico?.id) {
            setLaudoStatus({ message: 'ID do médico da avaliação não encontrado.', type: 'error' });
            return;
        }
        if (!estatisticas?.paciente?.id) {
            setLaudoStatus({ message: 'ID do paciente não encontrado nas estatísticas.', type: 'error' });
            return;
        }
        const payload = {
            ...laudoDataDoModal,
            medico_id: estatisticas.medico.id,
            paciente_id: estatisticas.paciente.id,
            avaliacao_id: avaliacaoId,
        };

        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');

        try {
            const responseLaudo = await fetch(`${baseUrl}/laudos`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`,
                },
                body: JSON.stringify(payload),
            });

            if (!responseLaudo.ok) {
                const errorData = await responseLaudo.json().catch(() => ({ message: 'Erro ao cadastrar laudo.' }));
                throw new Error(errorData.message || `Erro ${responseLaudo.status}`);
            }
            setLaudoStatus({ message: 'Laudo cadastrado com sucesso! Fechando avaliação...', type: 'info' });
            handleCloseLaudoModal();
            await handleCloseAvaliacao();

        } catch (error: any) {
            console.error("Erro no processo de laudo/fechamento:", error);
            setLaudoStatus({ message: error.message || 'Falha no processo de cadastro do laudo.', type: 'error' });
        }
    };

    const togglePdfViewer = (): void => {
        if (!avaliacaoId) return;
        setShowPdfViewer(!showPdfViewer);
    };

    const handleCloseAvaliacao = async () => {
        if (!avaliacaoId) {
            setLaudoStatus({ message: 'ID da avaliação não encontrado.', type: 'error' });
            return;
        }

        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem('@App:token');

        try {
            const response = await fetch(`${baseUrl}/avaliacoes/${avaliacaoId}/fechar`, {
                method: 'PUT',
                headers: { 'Authorization': `Bearer ${token}` }
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({ message: 'Erro ao fechar avaliação.' }));
                throw new Error(errorData.message || `Erro ${response.status}`);
            }

            setLaudoStatus({ message: 'Avaliação fechada com sucesso!', type: 'success' });
            fetchEstatisticas();
        } catch (error: any) {
            console.error('Erro ao fechar avaliação:', error);
            setLaudoStatus({ message: error.message || 'Falha ao fechar a avaliação.', type: 'error' });
        }
    };

    const toggleSessao = (sessaoId: string) => {
        setExpandedSessoes(prev => ({
            ...prev,
            [sessaoId]: !prev[sessaoId]
        }));
    };

    const toggleBateria = (bateriaId: string) => {
        setExpandedBaterias(prev => ({
            ...prev,
            [bateriaId]: !prev[bateriaId]
        }));
    };

    const prepareSessionChartData = (sessao: SessaoDetalhada) => {
        if (!sessao.is_plotavel || !sessao.estatisticas_sessao) return [];

        const data: { alternativa: string; contagem: number }[] = [];
        const alternativaCount: Record<string, number> = {};

        sessao.perguntas_com_respostas.forEach(pergunta => {
            if (pergunta.estatisticas_alternativas_pergunta) {
                pergunta.estatisticas_alternativas_pergunta.forEach(alt => {
                    if (!alternativaCount[alt.alternativa_texto]) {
                        alternativaCount[alt.alternativa_texto] = 0;
                    }
                    alternativaCount[alt.alternativa_texto] += alt.contagem_absoluta;
                });
            }
        });

        Object.keys(alternativaCount).forEach(altText => {
            data.push({
                alternativa: altText,
                contagem: alternativaCount[altText]
            });
        });

        return data.sort((a, b) => b.contagem - a.contagem);
    };

    const renderStatChip = (label: string, value: string | number, color?: "primary" | "secondary" | "default") => (
        <Chip
            label={`${label}: ${value}`}
            color={color || "default"}
            variant="outlined"
            sx={{
                fontWeight: 600,
                borderWidth: 1.5,
                borderColor: color ? theme.palette[color as 'primary' | 'secondary'].main : undefined
            }}
        />
    );

    const renderSessao = (sessao: SessaoDetalhada) => {
        const sessionChartData = prepareSessionChartData(sessao);
        const isPerguntasExpanded = !!expandedSessoes[sessao.id];

        return (
            <Card key={sessao.id} sx={{ mb: 2, borderLeft: `4px solid ${theme.palette.primary.light}` }} elevation={2}>
                <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Typography variant="h6" sx={{ fontWeight: 600 }}>
                            {sessao.titulo}
                            <Chip
                                label={sessao.is_plotavel ? "Plotável" : "Não Plotável"}
                                color={sessao.is_plotavel ? "success" : "default"}
                                size="small"
                                sx={{ ml: 1, fontWeight: 500 }}
                            />
                        </Typography>

                        <Tooltip title={isPerguntasExpanded ? "Ocultar detalhes das perguntas" : "Ver detalhes das perguntas"}>
                            <IconButton onClick={(event) => {
                                event.stopPropagation();
                                toggleSessao(sessao.id);
                            }} size="small">
                                <ExpandMoreIcon sx={{
                                    transform: isPerguntasExpanded ? 'rotate(180deg)' : 'none',
                                    transition: 'transform 0.3s'
                                }} />
                            </IconButton>
                        </Tooltip>
                    </Box>

                    {sessao.is_plotavel && sessao.estatisticas_sessao && (
                        <Box sx={{ mt: 2 }}>
                            <Box sx={{ mb: 2 }}>
                                <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                                    Estatísticas da Sessão
                                </Typography>
                                <Stack direction="row" spacing={1} flexWrap="wrap" useFlexGap sx={{ mb: 2 }}>
                                    {renderStatChip("Pontuação",
                                        `${sessao.estatisticas_sessao.total_pontuacao_obtida.toFixed(2)}/${sessao.estatisticas_sessao.total_pontuacao_maxima_possivel.toFixed(2)}`)}

                                    {renderStatChip("Aproveitamento",
                                        `${sessao.estatisticas_sessao.percentual_aproveitamento.toFixed(1)}%`, "primary")}

                                    {renderStatChip("Média",
                                        sessao.estatisticas_sessao.media_pontuacao_obtida_por_pergunta_respondida.toFixed(2))}

                                    {renderStatChip("Moda",
                                        getModaLabel(sessao.estatisticas_sessao.moda_pontuacao_obtida_nas_perguntas))}
                                </Stack>
                            </Box>

                            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
                                <Box sx={{ width: '100%', maxWidth: { xs: '100%', sm: 400, md: 500 }, height: isMobile ? 280 : 250, p: 1, border: `1px solid ${theme.palette.divider}`, borderRadius: 1 }}>
                                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1, textAlign: 'center' }}>
                                        Composição da Pontuação
                                    </Typography>
                                    <ResponsiveContainer width="100%" height="85%">
                                        <PieChart>
                                            <Pie
                                                data={[
                                                    { name: 'Pontuação Obtida', value: sessao.estatisticas_sessao.total_pontuacao_obtida },
                                                    { name: 'Restante', value: Math.max(0, sessao.estatisticas_sessao.total_pontuacao_maxima_possivel - sessao.estatisticas_sessao.total_pontuacao_obtida) }
                                                ]}
                                                cx="50%"
                                                cy="50%"
                                                innerRadius={isMobile ? 40 : 60}
                                                outerRadius={isMobile ? 70 : 90}
                                                fill="#8884d8"
                                                dataKey="value"
                                                label={({ name, percent }) => isMobile ? `${(percent * 100).toFixed(0)}%` : `${name}: ${(percent * 100).toFixed(0)}%`}
                                            >
                                                <Cell fill={COLORS_PIE[0]} />
                                                <Cell fill={COLORS_PIE[1]} />
                                            </Pie>
                                            <RechartsTooltip formatter={(value: number) => [value.toFixed(2), 'Valor']} />
                                            <Legend
                                                verticalAlign={isMobile ? "bottom" : "middle"}
                                                align={isMobile ? "center" : "right"}
                                                layout={isMobile ? "horizontal" : "vertical"}
                                                wrapperStyle={isMobile ? { paddingTop: '10px', fontSize: '0.8rem' } : { paddingLeft: '10px' }}
                                            />
                                        </PieChart>
                                    </ResponsiveContainer>
                                </Box>
                            </Box>
                            {sessionChartData.length > 0 && (
                                <Box sx={{ mt: 3, p: 1, border: `1px solid ${theme.palette.divider}`, borderRadius: 1 }}>
                                    <Typography variant="subtitle2" sx={{ fontWeight: 600, mb: 1 }}>
                                        Distribuição Geral de Respostas na Sessão
                                    </Typography>
                                    <Box sx={{ height: 300, mt: 1 }}>
                                        <ResponsiveContainer width="100%" height="100%">
                                            <BarChart
                                                data={sessionChartData}
                                                layout="vertical"
                                                margin={{ top: 5, right: isMobile ? 15 : 30, left: isMobile ? 20 : 100, bottom: isMobile ? 40 : 20 }}
                                            >
                                                <CartesianGrid strokeDasharray="3 3" />
                                                <XAxis type="number" tick={{ fontSize: isMobile ? '0.7rem' : '0.8rem' }} />
                                                <YAxis
                                                    dataKey="alternativa"
                                                    type="category"
                                                    width={isMobile ? 80 : 120}
                                                    tick={{ fontSize: isMobile ? '0.65rem' : '0.8rem', width: isMobile ? 70 : 110 }}
                                                    interval={0}
                                                />
                                                <RechartsTooltip formatter={(value: number) => [`${value} respostas`, '']} />
                                                <Legend wrapperStyle={isMobile ? { fontSize: '0.7rem', paddingTop: '10px' } : {}} verticalAlign={isMobile ? "bottom" : "top"} align="center" />
                                                <Bar
                                                    dataKey="contagem"
                                                    name="Frequência"
                                                    fill={theme.palette.primary.main}
                                                    radius={[0, 4, 4, 0]}
                                                >
                                                    {sessionChartData.map((_entry, index) => (
                                                        <Cell
                                                            key={`cell-${index}`}
                                                            fill={COLORS_BAR[index % COLORS_BAR.length]}
                                                        />
                                                    ))}
                                                </Bar>
                                            </BarChart>
                                        </ResponsiveContainer>
                                    </Box>
                                </Box>
                            )}
                        </Box>
                    )}

                    <Accordion
                        expanded={isPerguntasExpanded}
                        onChange={(event, newExpandedState) => {
                            event.stopPropagation();
                            setExpandedSessoes(prev => ({ ...prev, [sessao.id]: newExpandedState }));
                        }}
                        sx={{
                            mt: 2,
                            border: '1px solid',
                            borderColor: isPerguntasExpanded ? theme.palette.primary.main : theme.palette.divider,
                            borderRadius: 1,
                            boxShadow: 'none'
                        }}
                    >
                        <AccordionSummary
                            expandIcon={<ExpandMoreIcon />}
                            aria-controls={`sessao-detalhes-perguntas-${sessao.id}-content`}
                            sx={{
                                backgroundColor: isPerguntasExpanded ? theme.palette.action.hover : 'transparent',
                                '&:hover': { backgroundColor: theme.palette.action.selected }
                            }}
                        >
                            <Typography sx={{ display: 'flex', alignItems: 'center' }}>
                                <BarChartIcon sx={{ mr: 1, fontSize: '1.2rem' }} />
                                Detalhes das Perguntas
                            </Typography>
                        </AccordionSummary>

                        <AccordionDetails
                            id={`sessao-detalhes-perguntas-${sessao.id}-content`}
                            sx={{ pt: 2, backgroundColor: theme.palette.grey[50] }}
                        >
                            {sessao.perguntas_com_respostas.map(pergunta => (
                                <Box
                                    key={pergunta.pergunta_id}
                                    sx={{
                                        mb: 2,
                                        p: 2,
                                        borderRadius: 1,
                                        border: '1px solid',
                                        borderColor: theme.palette.divider,
                                        backgroundColor: 'white'
                                    }}
                                >
                                    <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                                        {pergunta.pergunta_texto}
                                    </Typography>

                                    <Typography variant="body2" sx={{ mt: 1, color: pergunta.resposta_texto ? 'text.primary' : 'error.main' }}>
                                        <strong>Resposta:</strong> {pergunta.resposta_texto || 'Não respondida'}
                                    </Typography>

                                    {sessao.is_plotavel && pergunta.pontuacao_maxima_possivel_pergunta !== undefined && (
                                        <Typography variant="body2" sx={{ mt: 0.5 }}>
                                            <strong>Pontuação:</strong> {pergunta.resposta_valor_escolhido ?? 0} / {pergunta.pontuacao_maxima_possivel_pergunta}
                                        </Typography>
                                    )}
                                </Box>
                            ))}
                        </AccordionDetails>
                    </Accordion>
                </CardContent>
            </Card>
        );
    };

    const renderBateria = (bateria: BateriaDetalhada, tipoBateriaLabel: string, isPerfilSaude = false) => {
        const isExpanded = !!expandedBaterias[bateria.id];

        return (
            <Card key={bateria.id} sx={{ mb: 3 }} elevation={3}>
                <CardContent>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                        <Box>
                            <Typography variant="h6" sx={{ fontWeight: 700, color: isPerfilSaude ? 'primary.main' : 'secondary.main' }}>
                                {bateria.questionario.titulo}
                            </Typography>

                            <Typography
                                variant="caption"
                                sx={{
                                    mt: 0.5,
                                    fontWeight: 500,
                                    color: isPerfilSaude ? theme.palette.primary.dark : theme.palette.secondary.dark,
                                    display: 'block'
                                }}
                            >
                                {tipoBateriaLabel}
                            </Typography>
                            <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                                Data: {formatDate(bateria.data_aplicacao)}
                            </Typography>
                        </Box>

                        <Button
                            variant="outlined"
                            size="small"
                            onClick={() => toggleBateria(bateria.id)}
                            endIcon={<ExpandMoreIcon sx={{ transform: isExpanded ? 'rotate(180deg)' : 'none' }} />}
                            sx={{
                                whiteSpace: 'nowrap',
                                flexShrink: 0,
                            }}
                        >
                            {isExpanded ? 'Ocultar Sessões' : 'Ver Sessões'}
                        </Button>
                    </Box>

                    <Divider sx={{ my: 2 }} />

                    {isExpanded && (
                        <Box sx={{ mt: 2 }}>
                            {bateria.sessoes_detalhadas.map(sessao => renderSessao(sessao))}
                        </Box>
                    )}
                </CardContent>
            </Card>
        );
    };

    if (loading) {
        return (
            <MedicoLayout>
                <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
                    <CircularProgress size={60} />
                </Box>
            </MedicoLayout>
        );
    }

    if (!estatisticas) {
        return (
            <MedicoLayout>
                <Typography variant="h6" color="error" sx={{ textAlign: 'center', mt: 4 }}>
                    Não foi possível carregar as estatísticas.
                </Typography>
                <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
                    <Button variant="contained" onClick={fetchEstatisticas}>
                        Tentar novamente
                    </Button>
                </Box>
            </MedicoLayout>
        );
    }

    return (
        <MedicoLayout>
            <Box sx={{ p: { xs: 1, sm: 2, md: 3 } }}>
                <Paper elevation={3} sx={{ p: { xs: 2, md: 3 }, mb: 3 }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: 1, mb: 2 }}>
                        <Typography variant="h4" component="h1" sx={{ fontWeight: 700, color: theme.palette.primary.dark }}>
                            Relatório de Avaliação
                        </Typography>
                        {estatisticas?.fechada && (
                            <Chip
                                label="Fechada"
                                size="small"
                                sx={{ backgroundColor: theme.palette.grey[300], color: theme.palette.text.secondary, fontWeight: 'medium' }}
                            />
                        )}
                        {estatisticas && !estatisticas.fechada && (
                            <Chip label="Aberta" color="success" variant="outlined" size="small" sx={{ fontWeight: 'medium' }} />
                        )}
                    </Box>
                    <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, justifyContent: 'space-between', flexWrap: 'wrap', gap: 2 }}>
                        <Box>
                            <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>
                                <strong>Paciente:</strong> {estatisticas.paciente_nome}
                            </Typography>
                        </Box>
                        <Box>
                            <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>
                                <strong>Data:</strong> {formatDate(estatisticas.data_avaliacao)}
                            </Typography>
                        </Box>
                        <Box>
                            <Typography variant="subtitle1" sx={{ fontWeight: 500 }}>
                                <strong>Avaliação ID:</strong> {estatisticas.avaliacao_id}
                            </Typography>
                        </Box>
                    </Box>
                    <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-start', gap: 2, flexWrap: 'wrap' }}>
                        {hasExames === null ? (
                            <Typography variant="body2" color="textSecondary">Verificando exames...</Typography>
                        ) : hasExames ? (
                            <Button
                                variant="contained"
                                color="secondary"
                                startIcon={<DownloadIcon />}
                                onClick={handleDownloadAllExames}
                                disabled={loading}
                            >
                                {loading && avaliacaoId ? 'Baixando...' : 'Baixar Todos os Exames da Avaliação'}
                            </Button>
                        ) : (
                            <Typography variant="body2" color="textSecondary">Nenhum exame disponível para download nesta avaliação.</Typography>
                        )}
                        <Button
                            variant="contained"
                            color="primary"
                            onClick={handleOpenLaudoModal}
                            disabled={!estatisticas?.paciente || !estatisticas?.medico || loading || estatisticas?.fechada}
                        >
                            Cadastrar Laudo
                        </Button>
                        {avaliacaoId && estatisticas?.fechada && (
                            <Button
                                variant="outlined"
                                color="info"
                                onClick={togglePdfViewer}
                                disabled={loading}
                            >
                                {showPdfViewer ? "Ocultar Laudo PDF" : "Visualizar Laudo PDF"}
                            </Button>
                        )}
                    </Box>
                </Paper>

                {showPdfViewer && avaliacaoId && estatisticas?.fechada && (
                    <Paper elevation={3} sx={{ mt: 3, p: 1, height: '90vh', overflow: 'hidden' }}>
                        <LaudoPDFViewer avaliacaoId={avaliacaoId} />
                    </Paper>
                )}

                {estatisticas.perfil_de_saude_detalhado && (
                    renderBateria(estatisticas.perfil_de_saude_detalhado, "Perfil de Saúde", true)
                )}

                {estatisticas.outras_baterias.length > 0 && (
                    <>
                        <Divider sx={{ my: 4 }}>
                            <Chip label="Outras Baterias Aplicadas" sx={{ fontSize: '1.1rem' }} />
                        </Divider>

                        {estatisticas.outras_baterias.map(bateria => (
                            renderBateria(bateria, "Bateria de Testes", false)
                        ))}
                    </>
                )}

                {!estatisticas.perfil_de_saude_detalhado && estatisticas.outras_baterias.length === 0 && (
                    <Paper elevation={2} sx={{ p: 3, mt: 3, textAlign: 'center' }}>
                        <Typography variant="h6" color="textSecondary">
                            Nenhuma bateria de testes encontrada para esta avaliação
                        </Typography>
                    </Paper>
                )}
            </Box>

            {isLaudoModalOpen && estatisticas?.paciente && estatisticas?.medico && (
                <LaudoCadastroModal
                    isOpen={isLaudoModalOpen}
                    onClose={handleCloseLaudoModal}
                    onSubmit={handleSubmitLaudo}
                    medico={estatisticas.medico}
                    paciente={estatisticas.paciente}
                    initialData={{}}
                />
            )}

            {laudoStatus && (
                <Snackbar open={!!laudoStatus} autoHideDuration={6000} onClose={() => setLaudoStatus(null)} anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}>
                    <Alert onClose={() => setLaudoStatus(null)} severity={laudoStatus.type as 'success' | 'error' | 'info'} sx={{ width: '100%' }}>{laudoStatus.message}</Alert>
                </Snackbar>
            )}
        </MedicoLayout>
    );
}
