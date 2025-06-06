import {
    Modal,
    Box,
    Typography,
    useTheme,
    Tooltip,
    Button,
    IconButton,
    TextField,
} from "@mui/material";
import { Questionario } from "../types/questionario";
import SearchBar from "../components/SearchBar";
import { useEffect, useState } from "react";
import ClearIcon from '@mui/icons-material/Clear'; // Importar o ícone de limpar

interface BateriasCadastroModalProps {
    open: boolean;
    onSubmit: (questionarioId: string, data_aplicacao: string) => void;
    onClose: () => void;
}

export default function BateriasCadastroModal({
    open,
    onSubmit,
    onClose,
}: BateriasCadastroModalProps) {
    const theme = useTheme();
    const [questionarios, setQuestionarios] = useState<Questionario[]>([]);
    const [questionarioSelecionado, setQuestionarioSelecionado] =
        useState<Questionario | null>(null);
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [isExpanded, setIsExpanded] = useState(false);
    const [date, setDate] = useState<string>(new Date().toISOString().split("T")[0]);

    const fetchSearchQuestionarios = async () => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");
        if (searchQuery.length < 3) {
            setQuestionarios([]);

            return;
        }
        fetch(
            `${baseUrl}/questionario/find_by_title_or_description/${searchQuery}`,
            {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    Authorization: `Bearer ${token}`,
                },
            }
        )
            .then((response) => response.json())
            .then((data) => {
                setQuestionarios(data);
            })
            .catch((error) => {
                console.error("Error fetching questionarios:", error);
            });
    };

    useEffect(() => {
        setQuestionarios([]);
    }, [open]);


    useEffect(() => {
        fetchSearchQuestionarios();
    }, [searchQuery]);

    useEffect(() => {
        // Expande se houver busca ativa e nada selecionado
        if (searchQuery.length >= 3 && !questionarioSelecionado) {
            setIsExpanded(true);
        } else {
            // Retrai se não houver busca suficiente ou se algo estiver selecionado
            setIsExpanded(false);
        }
    }, [searchQuery, questionarioSelecionado]);

    return (
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="modal-modal-title"
            aria-describedby="modal-modal-description"
        >
            <Box
                sx={{
                    position: "absolute",
                    top: "50%",
                    left: "50%",
                    transform: "translate(-50%, -50%)",
                    width: 400,
                    boxShadow: 24,
                    p: 4,
                    backgroundColor: theme.palette.background.default,
                    display: "flex",
                    flexDirection: "column",
                    alignItems: "center",
                    borderRadius: 2,
                }}
            >
                
                <Box
                    sx={{
                        display: "flex",
                        alignItems: "center",
                        width: "100%",
                        justifyContent: "center",
                        marginBottom: 2,
                        paddingBottom: 2,
                    }}
                >
                    <Box
                        sx={{
                            display: "flex",
                            justifyContent: "space-between",
                            width: "100%",
                        }}
                    >
                        <Box>
                            <Typography id="modal-modal-title" variant="h6" component="h2">
                                Cadastro de Baterias
                            </Typography>

                        </Box>
                        <Box
                        
                            sx={{

                                backgroundColor: theme.palette.error.main,
                                borderRadius: 1,
                                paddingX: 2,
                                paddingY: 1,
                                cursor: "pointer",
                                "&:hover": {
                                    backgroundColor: theme.palette.error.dark,
                                },
                            }}

                            onClick={onClose}
                            
                            >
                            <Typography color="white">X</Typography>
                        </Box>


                    </Box>

                </Box>
                <SearchBar onSearch={setSearchQuery} />

                <Box
                id="search-results"
                    sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        marginTop: 2,
                        width: "90%", // Ajustado para melhor aproveitamento
                        maxHeight: isExpanded ? '50vh' : (questionarioSelecionado ? '150px' : '80px'), // Altura dinâmica
                        transition: 'max-height 0.4s ease-in-out', // Animação
                        marginBottom: 2,
                        padding: isExpanded ? 2 : 1, // Padding menor quando retraído
                        border: "1px solid #ccc",
                        overflowY: "auto", // Scroll para a lista expandida
                        borderRadius: 2,
                    }}
                >
                    {questionarioSelecionado && !isExpanded ? (
                        <Box sx={{ padding: 1, width: '100%', textAlign: 'center' }}>
                            <Typography variant="subtitle2" sx={{ mb: 1 }}>Selecionado:</Typography>
                            <Box
                                sx={{
                                    border: `2px solid ${theme.palette.primary.main}`,
                                    borderRadius: 2,
                                    padding: "8px 16px", // Ajuste o padding
                                    backgroundColor: theme.palette.action.selected,
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                }}
                               
                            >
                                <Typography>{questionarioSelecionado.titulo}</Typography>
                                <Tooltip title="Limpar seleção">
                                    <IconButton size="small" onClick={() => setQuestionarioSelecionado(null)}>
                                        <ClearIcon fontSize="small" />
                                    </IconButton>
                                </Tooltip>
                            </Box>
                        </Box>
                    ) : isExpanded ? (
                        questionarios.length > 0 ? (
                            questionarios.map((questionario) => (
                                <Tooltip
                                    title={questionario.descricao || "Sem descrição"}
                                    key={questionario.id}
                                    placement="right"
                                    arrow
                                >
                                    <Box
                                        component={"button"}
                                        sx={{
                                            width: "100%",
                                            display: "flex",
                                            justifyContent: "space-between",
                                            alignItems: "center",
                                            marginBottom: 1,
                                            border: "1px solid #ccc", // Borda padrão
                                            borderRadius: 2,
                                            padding: 1,
                                            cursor: "pointer",
                                            backgroundColor: "transparent", // Fundo padrão
                                            "&:hover": {
                                                backgroundColor: theme.palette.action.hover,
                                                borderColor: theme.palette.primary.light,
                                            },
                                        }}
                                        onClick={() => setQuestionarioSelecionado(questionario)}
                                                                            >
                                        <Typography>{questionario.titulo}</Typography>
                                    </Box>
                                </Tooltip>
                            ))
                        ) : (
                            <Typography sx={{ textAlign: 'center', width: '100%', p: 1 }}>Nenhum questionário encontrado.</Typography>
                        )
                    ) : (
                        <Typography variant="caption" sx={{ textAlign: 'center', width: '100%', p: 1 }}>
                            Digite ao menos 3 caracteres para buscar.
                        </Typography>
                    )}
                </Box>

                <TextField
                    fullWidth
                    type="date"
                    label="Data de Aplicação"
                    value={date}
                    onChange={(e) => setDate(e.target.value)}
                    slotProps={{
                        inputLabel:{
                            shrink: true
                        }
                    }}
                    sx={{
                        marginBottom: 2,
                        marginTop: 2,
                        width: "95%",
                    }}
                    />
                <Button
                    variant="contained"
                    color="primary"
                    fullWidth
                    onClick={() => {
                        if (!questionarioSelecionado) {
                            return;
                        }

                        onSubmit(questionarioSelecionado.id, date);
                        onClose();
                    }}
                >
                    Salvar
                </Button>
            </Box>
        </Modal>
    );
}
