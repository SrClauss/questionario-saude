import {
    Modal,
    Box,
    Typography,
    useTheme,
    Tooltip,
    Button,
    IconButton,
} from "@mui/material";
import { Medico } from "../types/user"; // Assuming Medico type is in types/user
import SearchBar from "../components/SearchBar";
import { useEffect, useState } from "react";
import ClearIcon from '@mui/icons-material/Clear';

interface AtribuirMedicoModalProps {
    open: boolean;
    avaliacaoId: string;
    onSubmit: (medicoId: string, avaliacaoId: string) => void;
    onClose: () => void;
}

export default function AtribuirMedicoModal({
    open,
    avaliacaoId,
    onSubmit,
    onClose,
}: AtribuirMedicoModalProps) {
    const theme = useTheme();
    const [medicos, setMedicos] = useState<Medico[]>([]);
    const [medicoSelecionado, setMedicoSelecionado] =
        useState<Medico | null>(null);
    const [searchQuery, setSearchQuery] = useState<string>("");
    const [isExpanded, setIsExpanded] = useState(false);

    const fetchSearchMedicos = async () => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");
        if (searchQuery.length < 3) {
            setMedicos([]);
            return;
        }
        try {
            // IMPORTANT: Replace with your actual backend endpoint for searching doctors
            // This example assumes an endpoint like /medicos/search_by_name/:query
            const response = await fetch(
                `${baseUrl}/medicos/filter_by_name/${searchQuery}`, // Placeholder endpoint
                {
                    method: "GET",
                    headers: {
                        "Content-Type": "application/json",
                        Authorization: `Bearer ${token}`,
                    },
                }
            );
            if (!response.ok) {
                // Handle non-OK responses (e.g., 404, 500)
                console.error("Error fetching medicos:", response.statusText);
                setMedicos([]); // Clear medicos on error
                return;
            }
            const data = await response.json();
            setMedicos(data as Medico[]); // Ensure data is cast to Medico[]
        } catch (error) {
            console.error("Error fetching medicos:", error);
            setMedicos([]); // Clear medicos on fetch error
        }
    };

    useEffect(() => {
        if (open) { // Reset state when modal opens
            setSearchQuery("");
            setMedicoSelecionado(null);
            setMedicos([]);
            setIsExpanded(false);
        }
    }, [open]);

    useEffect(() => {
        const debounceTimer = setTimeout(() => {
            if (searchQuery.length >= 3) {
                fetchSearchMedicos();
            } else {
                setMedicos([]);
            }
        }, 500); // Debounce API calls

        return () => clearTimeout(debounceTimer);
    }, [searchQuery]);

    useEffect(() => {
        if (searchQuery.length >= 3 && !medicoSelecionado) {
            setIsExpanded(true);
        } else {
            setIsExpanded(false);
        }
    }, [searchQuery, medicoSelecionado]);

    return (
        <Modal
            open={open}
            onClose={onClose}
            aria-labelledby="modal-atribuir-medico-title"
            aria-describedby="modal-atribuir-medico-description"
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
                        justifyContent: "space-between",
                        marginBottom: 2,
                    }}
                >
                    <Typography id="modal-atribuir-medico-title" variant="h6" component="h2">
                        Atribuir Médico Responsável
                    </Typography>
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
                <SearchBar onSearch={setSearchQuery} />

                <Box
                    id="search-results-medicos"
                    sx={{
                        display: "flex",
                        flexDirection: "column",
                        alignItems: "center",
                        marginTop: 2,
                        width: "100%",
                        maxHeight: isExpanded ? '50vh' : (medicoSelecionado ? 'auto' : '80px'),
                        transition: 'max-height 0.3s ease-in-out',
                        marginBottom: 2,
                        padding: isExpanded || medicoSelecionado ? 1 : 0,
                        border: isExpanded || medicoSelecionado ? "1px solid #ccc" : "none",
                        overflowY: "auto",
                        borderRadius: 2,
                    }}
                >
                    {medicoSelecionado && !isExpanded ? (
                        <Box sx={{ padding: 1, width: '100%', textAlign: 'center' }}>
                            <Typography variant="subtitle2" sx={{ mb: 1 }}>Selecionado:</Typography>
                            <Box
                                sx={{
                                    border: `2px solid ${theme.palette.primary.main}`,
                                    borderRadius: 2,
                                    padding: "8px 16px",
                                    backgroundColor: theme.palette.action.selected,
                                    display: "flex",
                                    justifyContent: "space-between",
                                    alignItems: "center",
                                }}
                            >
                                <Typography>{medicoSelecionado.nome}</Typography>
                                <Tooltip title="Limpar seleção">
                                    <IconButton size="small" onClick={() => { setMedicoSelecionado(null); setSearchQuery(""); /* Optionally re-trigger search or clear results */ }}>
                                        <ClearIcon fontSize="small" />
                                    </IconButton>
                                </Tooltip>
                            </Box>
                        </Box>
                    ) : isExpanded ? (
                        medicos.length > 0 ? (
                            medicos.map((medico) => (
                                <Tooltip title={medico.crm || medico.especialidade || "Detalhes não disponíveis"} key={medico.id} placement="right" arrow>
                                    <Box component={"button"} sx={{ width: "100%", display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: 1, border: "1px solid #ccc", borderRadius: 2, padding: 1, cursor: "pointer", backgroundColor: "transparent", "&:hover": { backgroundColor: theme.palette.action.hover, borderColor: theme.palette.primary.light, }, textAlign: 'left' }} onClick={() => setMedicoSelecionado(medico)}>
                                        <Typography>{medico.nome}</Typography>
                                    </Box>
                                </Tooltip>
                            ))
                        ) : (
                            <Typography sx={{ textAlign: 'center', width: '100%', p: 1 }}>Nenhum médico encontrado.</Typography>
                        )
                    ) : (
                        searchQuery.length < 3 && <Typography variant="caption" sx={{ textAlign: 'center', width: '100%', p: 1 }}>Digite ao menos 3 caracteres para buscar.</Typography>
                    )}
                </Box>

                <Button
                    variant="contained"
                    color="primary"
                    fullWidth
                    disabled={!medicoSelecionado}
                    onClick={() => {
                        if (medicoSelecionado) {
                            onSubmit(medicoSelecionado.id, avaliacaoId);
                        }
                    }}
                    sx={{ marginTop: 2 }}
                >
                    Atribuir Médico
                </Button>
            </Box>
        </Modal>
    );
} 