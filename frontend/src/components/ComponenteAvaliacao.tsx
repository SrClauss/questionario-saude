import { useEffect, useRef, useState } from "react";
import {
    Box,
    Button,
    Card,
    CardContent,
    CardHeader,
    Chip,
    CircularProgress,
    List,
    ListItem,
    ListItemText,
    Snackbar,
    IconButton,
    Paper,
    Stack,
    Tooltip,
    Typography,
} from "@mui/material";
import {
    Assignment,
    CalendarMonth,
    CheckCircleOutline,
    Comment,
    Description,
    HourglassEmpty,
    LibraryBooks,
    Delete as DeleteIcon, // Renomeado para evitar conflito se houver outro Delete
    Person,
    Upload,
} from "@mui/icons-material";
import { Paciente } from "../types/user"; // Adicionado Exame
import { Exame } from "../types/exame";
import { Avaliacao } from "../types/avaliacao";
import { Questionario } from "../types/questionario";
import { Alert } from "@mui/material";
import DeleteModal from "../modals/DeleteDialog"; // Importar o DeleteModal
import { useNavigate } from "react-router-dom"; // Importar useNavigate



interface ComponenteAvaliacaoProps {
    // Adicione um callback para ser chamado após a exclusão de um exame, se necessário para atualizar o pai
    onExameDeleted?: () => void; 
    avaliacaoJoin: AvaliacaoFetch;

}

export interface AvaliacaoFetch {
    avaliacao: Avaliacao;
    baterias_testes: BateriasTestesJoin[];
    paciente: Paciente;

}
interface BateriasTestesJoin {
    colaborador_id: string;
    created_at: string;
    data_aplicacao: string;
    id: string;
    is_completo: boolean;
    observacoes: string;
    paciente_id: string;
    profissional_saude_id: string;
    questionario_id: string;
    respostas: {};
    total_perguntas: number;
    updated_at: string;
    questionario: Questionario;

}



export default function ComponenteAvaliacao({ avaliacaoJoin, onExameDeleted }: ComponenteAvaliacaoProps) {
    const { avaliacao, baterias_testes, paciente } = avaliacaoJoin;
    const navigate = useNavigate(); // Hook para navegação
    const fileInputRef = useRef<HTMLInputElement>(null);
    const [isUploading, setIsUploading] = useState(false);
    const [snackbarOpen, setSnackbarOpen] = useState(false);
    const [snackbarMessage, setSnackbarMessage] = useState("");
    const [exames, setExames] = useState<Exame[]>([]);
    const [showDeleteExameModal, setShowDeleteExameModal] = useState(false);
    const [exameIdToDelete, setExameIdToDelete] = useState<string | null>(null);
    const [nomeExameToDelete, setNomeExameToDelete] = useState<string>("");
    const [totalExamesSize, setTotalExamesSize] = useState<number | null>(null);
    const [snackbarSeverity, setSnackbarSeverity] = useState<"success" | "error" | "info" | "warning">(
        "success"
    );
    
    // Função para formatar a data
    const formatDate = (dateString: string) => {
        if (!dateString) return 'N/A';
        try {
            return new Date(dateString).toLocaleDateString('pt-BR', { timeZone: 'UTC' });
        } catch {
            return 'Data inválida';
        }
    };

    // Função para formatar bytes em MB, KB, etc.
    const formatBytes = (bytes: number, decimals = 2) => {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const dm = decimals < 0 ? 0 : decimals;
        const sizes = ['Bytes', 'KB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
    };

    const handleFileSelect = () => {
        fileInputRef.current?.click();
    };

    const fetchExames = async () => {
        if (!avaliacao.id) return;
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");
        try {
            const response = await fetch(`${backendUrl}/exames/all_list/${avaliacao.id}`, { // Usando all_list conforme solicitado anteriormente
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.ok) {
                const data = await response.json();
                setExames(data);
            } else {
                console.error("Erro ao buscar exames:", await response.text());
                setExames([]);
            }
        } catch (error) {
            console.error("Erro de conexão ao buscar exames:", error);
            setExames([]);
        }
    };

    const fetchTotalExamesSize = async () => {
        if (!avaliacao.id) return;
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");
        try {
            const response = await fetch(`${backendUrl}/exames/total_size/${avaliacao.id}`, {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            });
            if (response.ok) {
                const data = await response.json();
                setTotalExamesSize(data.total_size_bytes);
            } else {
                console.error("Erro ao buscar tamanho total dos exames:", await response.text());
                setTotalExamesSize(null);
            }
        } catch (error) {
            console.error("Erro de conexão ao buscar tamanho total dos exames:", error);
            setTotalExamesSize(null);
        }
    };
    const handleFileUpload = async (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (!file) {
            return;
        }

        setIsUploading(true);
        const formData = new FormData();
        formData.append("file", file);
        formData.append("avaliacao_id", avaliacao.id);
        // Os campos nome_exame e descricao_exame foram removidos do backend para o modelo Exame atual

        // Usando a rota de criação de exames (ex: POST /exames/)
        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");

        try {
            const response = await fetch(`${backendUrl}/exames/`, { // Rota de criação de exames via Caddy
                method: "POST",
                headers: {
       Authorization: `Bearer ${token}`,
                },
                body: formData,
            });

            const data = await response.json();

            if (response.ok) {
                setSnackbarMessage(data.message || "Exame enviado com sucesso!");
                setSnackbarSeverity("success");
                fetchExames(); // Atualiza a lista de exames
                fetchTotalExamesSize(); // Atualiza o tamanho total
            } else {
                setSnackbarMessage(data.error || data.message || "Erro ao enviar exame.");
                setSnackbarSeverity("error");
            }
        } catch (error) {
            console.error("Erro no upload do exame:", error);
            setSnackbarMessage("Erro de conexão ao enviar exame.");
            setSnackbarSeverity("error");
        } finally {
            setIsUploading(false);
            setSnackbarOpen(true);
            // Limpa o valor do input para permitir o upload do mesmo arquivo novamente, se necessário
            if (fileInputRef.current) {
                fileInputRef.current.value = "";
            }
        }
    };

    const openDeleteConfirmationModal = (exame: Exame) => {
        const nomePacienteFormatado = paciente.nome.toUpperCase().replace(/ /g, '_');
        const dataExameFormatada = new Date(exame.created_at).toLocaleDateString('sv-SE').replace(/-/g, '');
        const nomeArquivo = `${dataExameFormatada}-${nomePacienteFormatado}-${exame.id}.pdf`;
        
        setExameIdToDelete(exame.id);
        setNomeExameToDelete(nomeArquivo);
        setShowDeleteExameModal(true);
    };

    const handleDeleteExame = async () => {
        if (!exameIdToDelete) return;

        const backendUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");

        try {
            const response = await fetch(`${backendUrl}/exames/${exameIdToDelete}`, {
                method: "DELETE",
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });

            if (response.ok) {
                setSnackbarMessage("Exame deletado com sucesso!");
                setSnackbarSeverity("success");
                fetchExames(); // Atualiza a lista de exames
                fetchTotalExamesSize(); // Atualiza o tamanho total
                if (onExameDeleted) onExameDeleted(); // Callback para o componente pai, se necessário
            } else {
                const data = await response.json();
                setSnackbarMessage(data.error || data.message || "Erro ao deletar exame.");
                setSnackbarSeverity("error");
            }
        } catch (error) {
            console.error("Erro ao deletar exame:", error);
            setSnackbarMessage("Erro de conexão ao deletar exame.");
            setSnackbarSeverity("error");
        } finally {
            setSnackbarOpen(true);
            setShowDeleteExameModal(false);
            setExameIdToDelete(null);
        }
    };

    useEffect(() => {
        if (avaliacao.id) {
            fetchExames();
            fetchTotalExamesSize();
        }
    }, [avaliacao.id]);

    return (
        <Paper elevation={6} sx={{ padding: 4, marginBottom: 4, borderRadius: '12px', bgcolor: 'background.paper' }}>
            <Box
                sx={{
                    display: 'flex',
                    flexDirection: { xs: 'column', md: 'row' }, // Empilha em telas pequenas, lado a lado em telas médias/grandes
                    gap: 3, // Espaçamento entre os cartões
                }}
            >
 
                <Box sx={{ flex: 1 }}> {/* Ocupa espaço disponível no flex container */}
                    <Card variant="outlined" sx={{ height: '100%', borderRadius: '8px' }}>
                        <CardHeader
                            title={
                                <Stack direction="row" alignItems="center" spacing={1}>
                                    <Assignment color="primary" />
                                    <Typography variant="h6" color="primary">
                                        Detalhes da Avaliação
                                    </Typography>
                                </Stack>
                            }
                            sx={{ pb: 0 }}
                        />
                        <CardContent>
                            <Stack spacing={1.5}>
                                <Box display="flex" alignItems="center" gap={1}>
                                    <CalendarMonth color="action" fontSize="small" />
                                    <Typography variant="body1">
                                        <strong>Iniciada em:</strong> {formatDate(avaliacao.data_inicio)}
                                    </Typography>
                                </Box>
                                <Box display="flex" alignItems="center" gap={1}>
                                    <Person color="action" fontSize="small" />
                                    <Typography variant="body1">
                                        <strong>Paciente:</strong> {paciente?.nome || "N/A"}
                                    </Typography>
                                </Box>
                                {avaliacao.laudo_id && (
                                    <Box display="flex" alignItems="center" gap={1}>
                                        <Description color="action" fontSize="small" />
                                        <Typography variant="body1">
                                            <strong>Laudo ID:</strong> {avaliacao.laudo_id}
                                        </Typography>
                                    </Box>
                                )}
                                <input
                                    type="file"
                                    hidden
                                    ref={fileInputRef}
                                    onChange={handleFileUpload}
                                    // Adicione accept se quiser restringir tipos de arquivo, ex: accept=".pdf,.jpg,.png"
                                />
                                <Button
                                    id="enviar-exames"
                                    fullWidth
                                    variant="contained"
                                    color="primary"
                                    startIcon={isUploading ? <CircularProgress size={20} color="inherit" /> : <Upload />}
                                    onClick={handleFileSelect}
                                    disabled={isUploading}
                                >
                                    {isUploading ? "Enviando..." : "Enviar Exames"}
                                </Button>

                                {exames.length > 0 && (
                                    <Box mt={2} width="100%">
                                        <Typography variant="subtitle2" gutterBottom sx={{ color: 'text.secondary' }}>
                                            Exames Enviados:
                                        </Typography>
                                        <List id="exames-list" dense sx={{ width: '100%', bgcolor: 'action.hover', borderRadius: 1, border: '1px solid', borderColor: 'divider', maxHeight: 200, overflow: 'auto', paddingBottom: 2 /* Adiciona padding ao final da lista */ }}>
                                            {exames.map((exame) => {
                                                const nomePacienteFormatado = paciente.nome.toUpperCase().replace(/ /g, '_');
                                                // Formata a data para YYYYMMDD
                                                const dataExameFormatada = new Date(exame.created_at).toLocaleDateString('sv-SE').replace(/-/g,'');
                                                const nomeArquivo = `${dataExameFormatada}-${nomePacienteFormatado}-${exame.id}.pdf`;

                                                return (
                                                    <ListItem
                                                        key={exame.id}
                                                        secondaryAction={
                                                            !avaliacao.fechada && (
                                                                <Tooltip title="Deletar Exame">
                                                                    <IconButton edge="end" aria-label="delete" onClick={() => openDeleteConfirmationModal(exame)}>
                                                                        <DeleteIcon color="error" fontSize="small" />
                                                                    </IconButton>
                                                                </Tooltip>
                                                            )
                                                        }
                                                        sx={{ '&:hover': { bgcolor: 'action.selected' } }}
                                                    >
                                                        <Tooltip title={nomeArquivo} placement="top-start">
                                                            <ListItemText
                                                                primary={nomeArquivo}
                                                                primaryTypographyProps={{
                                                                    sx: { overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap', display: 'block', maxWidth: { xs: 'calc(100% - 40px)', sm: 'calc(100% - 40px)' } }
                                                                }}
                                                            />
                                                        </Tooltip>
                                                    </ListItem>
                                                );
                                            })}
                                        </List>
                                        {totalExamesSize !== null && exames.length > 0 && (
                                            <Typography variant="caption" display="block" sx={{ mt: 1, color: 'text.secondary', textAlign: 'right' }}>
                                                Tamanho total dos exames: {formatBytes(totalExamesSize)}
                                            </Typography>
                                        )}
                                    </Box>
                                )}
                            </Stack>
                        </CardContent>
                    </Card>
                </Box>

                {/* Seção de Baterias de Testes */}
                <Box sx={{ flex: 1 }}> {/* Ocupa espaço disponível no flex container */}
                    <Card variant="outlined" sx={{ height: '100%', borderRadius: '8px' }}>
                        <CardHeader
                            title={
                                <Stack direction="row" alignItems="center" spacing={1}>
                                    <LibraryBooks color="primary" />
                                    <Typography variant="h6" color="primary">
                                        Baterias de Testes Aplicadas
                                    </Typography>
                                </Stack>
                            }
                            sx={{ pb: 0 }}
                        />
                        <CardContent>
                            <Stack spacing={2}>
                                {baterias_testes && baterias_testes.length > 0 ? (
                                    baterias_testes.map((bateria, index) => (
                                        <Box
                                            key={bateria.id || index}
                                            sx={{
                                                padding: 2,
                                                border: '1px solid',
                                                borderColor: 'divider',
                                                borderRadius: '6px',
                                                bgcolor: 'action.hover', // Cor de fundo sutil
                                                boxShadow: 1, // Sombra sutil
                                            }}
                                        >
                                            <Stack spacing={1}>
                                                <Typography variant="subtitle1" component="div" sx={{ fontWeight: 'bold', color: 'text.primary' }}>
                                                    <Stack direction="row" alignItems="center" spacing={1}>

                                                        <Box component={"span"} sx={{ display: { xs: 'none', md: 'block' } }}>
                                                            <Description fontSize="small" />
                                                        </Box>
                                                        {bateria.questionario?.titulo || "Não identificado"}
                                                    </Stack>
                                                </Typography>
                                                <Box display="flex" alignItems="center" gap={1}>
                                                    <CalendarMonth fontSize="small" color="action" />
                                                    <Typography variant="body2">
                                                        <strong>Data de Aplicação:</strong> {formatDate(bateria.data_aplicacao)}
                                                    </Typography>
                                                </Box>
                                                <Box display="flex" alignItems="center" gap={1}>
                                                    {bateria.is_completo ? (
                                                        <Chip
                                                            label="Completo"
                                                            color="success"
                                                            size="small"
                                                            icon={<CheckCircleOutline fontSize="small" />}
                                                        />
                                                    ) : (
                                                        <Chip
                                                            label="Incompleto"
                                                            color="warning"
                                                            size="small"
                                                            icon={<HourglassEmpty fontSize="small" />}
                                                        />
                                                    )}
                                                </Box>
                                                {bateria.observacoes && (
                                                    <Box display="flex" alignItems="flex-start" gap={1}>
                                                        <Comment fontSize="small" color="action" sx={{ mt: 0.5 }} />
                                                        <Typography variant="body2">
                                                            <strong>Observações:</strong> {bateria.observacoes}
                                                        </Typography>
                                                    </Box>
                                                )}
                                            </Stack>
                                        </Box>
                                    ))
                                ) : (
                                    <Typography variant="body2" sx={{ fontStyle: 'italic', color: 'text.secondary' }}>
                                        Nenhuma bateria de testes aplicada nesta avaliação.
                                    </Typography>
                                )}
                                <Box sx={{ mt: 2, display: 'flex', justifyContent: 'flex-end' }}>
                                    <Tooltip title="Ver detalhes dos testes aplicados nesta avaliação">
                                        <Button
                                            variant="contained"
                                            fullWidth
                                            size="small"
                                            onClick={() => navigate(`/paciente-baterias-list/${avaliacao.id}`)} // Navega para a rota com o ID da avaliação
                                        >
                                            Ver Testes da Avaliação
                                        </Button>
                                    </Tooltip>
                                </Box>
                            </Stack>
                        </CardContent>
                    </Card>
                </Box>
            </Box>
            <Snackbar
                open={snackbarOpen}
                autoHideDuration={6000}
                onClose={() => setSnackbarOpen(false)}
                anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
            >
                <Alert
                    onClose={() => setSnackbarOpen(false)}
                    severity={snackbarSeverity}
                    sx={{ width: "100%" }}
                >
                    {snackbarMessage}
                </Alert>
            </Snackbar>
            {/* Modal de Confirmação para Deletar Exame */}
            <DeleteModal
                open={showDeleteExameModal}
                onClose={() => setShowDeleteExameModal(false)}
                onConfirm={handleDeleteExame}
                itemName={nomeExameToDelete} // Passa o nome do arquivo do exame para itemName
            />
        </Paper>
    );
}