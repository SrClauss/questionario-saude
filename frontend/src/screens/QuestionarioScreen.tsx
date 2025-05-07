import React, { useState } from "react";
import {
    Box,
    Table,
    TableHead,
    TableRow,
    TableCell,
    TableBody,
    IconButton,
    Tooltip,
    Button,
    Snackbar,
    Alert
} from "@mui/material";
import { Delete, InfoRounded, Add } from "@mui/icons-material";
import SearchBar from "../components/SearchBar";
import AdminLayout from "../layouts/AdminLayout";
import { useNavigate } from "react-router-dom";
import DeleteModal from "../modals/DeleteDialog";

interface Questionario {
    id: string;
    titulo: string;
    // Outras propriedades podem existir, mas não serão exibidas
}

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
        onClose: () => {},
        onConfirm: () => {},
        itemName: "",
        id: ""
    });


    const handleFilter = (query: string) => {
        if (query.length < 3) return;
        setSearchQuery(query);

        const baseUrl = import.meta.env.VITE_BACKEND_URL;
        const token = localStorage.getItem("@App:token");
        const url = `${baseUrl}/questionario/find_by_title_or_description/${query}/`;

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
                        //uma espera de 2 segundos para redirecionar
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
                    setSnackbar({
                        open: true,
                        type: "success",
                        message: "Questionários carregados com sucesso!"
                    });
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

    return (
        <AdminLayout>
            <Box sx={{ marginBottom: 2 }}>
                <SearchBar onSearch={handleFilter} />
            </Box>
            <Box sx={{ display: "flex", justifyContent: "flex-end", marginBottom: 2 }}>
                <Button onClick={() => navigate("/cadastro-questionario")} variant="contained" color="primary" startIcon={<Add />}>
                    Cadastrar Questionário
                </Button>
            </Box>
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
                            <TableCell>{q.titulo}</TableCell>
                            <TableCell>
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
                            </TableCell>
                        </TableRow>
                    ))}
                </TableBody>
            </Table>
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
        </AdminLayout>
    );
}