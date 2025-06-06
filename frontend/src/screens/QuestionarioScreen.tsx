import { useState, useEffect } from "react";
import {
    Box,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
    IconButton,
    Tooltip,
    Snackbar,
    Alert,
    styled,
    Pagination,
    Fab
} from "@mui/material";
import { Delete, InfoRounded, Add, Person2 } from "@mui/icons-material";
import SearchBar from "../components/SearchBar";
import VariableLayout from "../layouts/VariableLayout";
import { useNavigate } from "react-router-dom";
import DeleteModal from "../modals/DeleteDialog";

import { Questionario } from "../types/questionario";
import StylizedTitle from "../components/StylizedTitle";

const StyledTableCell = styled(TableCell)(({ theme }) => ({
    overflow: 'hidden',
    textOverflow: 'ellipsis',
    whiteSpace: 'nowrap',
    maxWidth: 'calc(100% - 150px)', // Ajuste este valor conforme necessário
    flexGrow: 1,
    [theme.breakpoints.down('sm')]: {
        whiteSpace: 'normal', // Permite quebra de linha em telas menores
    },
}));

const ActionsTableCell = styled(TableCell)(({ theme }) => ({
    whiteSpace: 'nowrap',
    width: '150px', // Ajuste este valor conforme necessário
    [theme.breakpoints.down('sm')]: {
        width: '100%', // Ocupa toda a largura disponível
        display: 'flex',
        flexDirection: 'column', // Coloca os botões um embaixo do outro
        alignItems: 'flex-start', // Alinha os botões à esquerda
        whiteSpace: 'normal', // Permite quebra de linha nos textos dos botões, se necessário
    },
}));

export default function QuestionarioScreen() {
    const [questionarios, setQuestionarios] = useState<Questionario[]>([]);
    const [snackbar, setSnackbar] = useState({
        open: false,
        message: "",
        type: "info" as "error" | "success" | "info" | "warning"
    });
    const [searchQuery, setSearchQuery] = useState<string>("");
    const navigate = useNavigate();
    const handleSnackbarClose = () => {
        setSnackbar({ ...snackbar, open: false });
    };
    interface deleteModalProps {
        open: boolean;
        onClose: () => void;
        onConfirm: () => void;
        itemName?: string; // Nome do item a ser deletado (opcional)
        id?: string; // ID do item a ser deletado (opcional)
    }

    const [showDeleteModal, setShowDeleteModal] = useState<deleteModalProps>({
        open: false,
        onClose: () => { },
        onConfirm: () => { },
        itemName: "",
        id: ""
    });

    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const itemsPerPage = 10;
    const [aplicacaoModal, setAplicacaoModal] = useState({
        open: false,
        questionario: {} as Questionario,
        onClose: () => { setAplicacaoModal({ ...aplicacaoModal, open: false }) },
    });


    const fetchQuestionarios = (query: string = "", currentPage: number = 1) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");
        let url = `${baseUrl}/questionario`;

        if (query) {
            url = `${baseUrl}/questionario/find_by_title_or_description/${query}`;
        } else {
            url = `${baseUrl}/questionario/${currentPage}/${itemsPerPage}`;
        }

        fetch(url, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })
            .then((response) => {
                if (!response.ok) {
                    if (response.status === 401) {
                        setSnackbar({
                            open: true,
                            type: "error",
                            message: "Sessão expirada. Faça login novamente."
                        });
                        localStorage.removeItem("@App:token");
                        setTimeout(() => {
                            navigate("/login");
                        }, 2000);
                        return;
                    }
                    throw new Error(`Erro na requisição: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                if (Array.isArray(data)) {
                    setQuestionarios(data);
                    setTotalPages(Math.ceil(30 / itemsPerPage));
                } else {
                    console.error("API retornou um formato inesperado:", data);
                    setSnackbar({
                        open: true,
                        type: "error",
                        message: "Erro ao buscar questionários: Formato de resposta inválido"
                    });
                }
            })
            .catch((error) => {
                console.error("Error fetching questionários:", error);
                setSnackbar({
                    open: true,
                    type: "error",
                    message: `Erro ao buscar questionários: ${error}`
                });
            });
    };

    const handleFilter = (query: string) => {
        setSearchQuery(query);
        setPage(1); // Reset para a primeira página ao realizar uma nova busca
        fetchQuestionarios(query, 1);
    };

    useEffect(() => {
        fetchQuestionarios("", page); // Carrega a primeira página ao montar o componente
    }, [page]);

    const handleDelete = (id: string) => {
        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");
        const url = `${baseUrl}/questionario/${id}`;

        fetch(url, {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            }
        })
            .then((response) => {
                if (!response.ok) {
                    throw new Error(`Erro na requisição: ${response.status}`);
                }
                return response.json();
            })
            .then((data) => {
                setSnackbar({
                    open: true,
                    type: "success",
                    message: data.message || "Questionário deletado com sucesso"
                });
                if (searchQuery) {
                    handleFilter(searchQuery);
                }
            })
            .catch((error) => {
                console.error("Error deleting questionário:", error);
                setSnackbar({
                    open: true,
                    type: "error",
                    message: `Erro ao deletar questionário: ${error.message}`
                });
            });
    };

    const handleChangePage = (_event: any, value: number) => {
        setPage(value);
    };

    return (
        <VariableLayout>
            <Box id="container"

            sx={{
                paddingTop:{ xs: 4, sm: 4, md: 0 },
            }}
            >
                <StylizedTitle title="Questionários" />
                <Box >
                    <SearchBar onSearch={handleFilter} />
                </Box>
                <Fab
                    color="primary"
                    aria-label="add"
                    onClick={() => navigate("/cadastro-questionario")}
                    sx={{
                        position: 'fixed',
                        bottom: 16,
                        right: 32,
                    }}
                >
                    <Add />

                </Fab>
               
               
                <Table>
                    <TableHead>
                        <TableRow>
                            <TableCell>Título</TableCell>
                            <TableCell>Ações</TableCell>
                        </TableRow>
                    </TableHead>
                    <TableBody>
                        {questionarios.map((q) => (
                            <TableRow key={q.id}>
                                <StyledTableCell>
                                    {q.titulo}
                                </StyledTableCell>
                                <ActionsTableCell>
                                   
                                    <Tooltip title="Info">
                                        <IconButton color="info" onClick={() => navigate(`/cadastro-questionario/${q.id}`)}>
                                            <InfoRounded />
                                        </IconButton>
                                    </Tooltip>
                                    <Tooltip title="Delete">
                                        <IconButton
                                            color="error"
                                            onClick={() => setShowDeleteModal({
                                                open: true,
                                                onClose: () => setShowDeleteModal({ ...showDeleteModal, open: false }),
                                                onConfirm: () => handleDelete(q.id),
                                                itemName: q.titulo,
                                                id: q.id
                                            })}
                                        >
                                            <Delete />
                                        </IconButton>
                                    </Tooltip>
                                </ActionsTableCell>
                            </TableRow>
                        ))}
                    </TableBody>
                </Table>
                <Box sx={{ display: 'flex', justifyContent: 'center', marginTop: 2 }}>
                    <Pagination
                        count={totalPages}
                        page={page}
                        onChange={handleChangePage}
                        color="primary"
                    />
                </Box>
                <Snackbar
                    open={snackbar.open}
                    autoHideDuration={6000}
                    onClose={handleSnackbarClose}
                    anchorOrigin={{ vertical: "bottom", horizontal: "center" }}
                >
                    <Alert
                        onClose={handleSnackbarClose}
                        severity={snackbar.type}
                        sx={{ width: "100%" }}
                    >
                        {snackbar.message}
                    </Alert>
                </Snackbar>
                <DeleteModal
                    open={showDeleteModal.open}
                    onClose={() => setShowDeleteModal({ ...showDeleteModal, open: false })}
                    onConfirm={() => {
                        handleDelete(showDeleteModal.id || "");
                        setShowDeleteModal({ ...showDeleteModal, open: false });
                    }}
                    itemName={showDeleteModal.itemName}
                />

            </Box>
        </VariableLayout>
    );
}